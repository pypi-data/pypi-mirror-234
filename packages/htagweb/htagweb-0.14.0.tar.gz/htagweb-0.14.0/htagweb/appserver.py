# -*- coding: utf-8 -*-
# #############################################################################
# Copyright (C) 2023 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/htagweb
# #############################################################################

# gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b localhost:8000 --preload basic:app


import os
import sys
import json
import uuid
import logging
import uvicorn
import asyncio
import hashlib
import multiprocessing
from htag import Tag
from starlette.applications import Starlette
from starlette.responses import HTMLResponse,PlainTextResponse
from starlette.applications import Starlette
from starlette.routing import Route,WebSocketRoute
from starlette.endpoints import WebSocketEndpoint
from starlette.middleware import Middleware
from starlette.requests import HTTPConnection
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from htag.runners import commons
from . import crypto
import redys.v2

from htagweb.server import hrserver, hrserver_orchestrator, kill_hrserver, wait_hrserver
from htagweb.server.client import HrClient

logger = logging.getLogger(__name__)
####################################################
from types import ModuleType

from . import sessions

def findfqn(x) -> str:
    if isinstance(x,str):
        if ("." not in x) and (":" not in x):
            raise Exception(f"'{x}' is not a 'full qualified name' (expected 'module.name') of an App (htag.Tag class)")
        return x    # /!\ x is a fqn /!\ DANGEROUS /!\
    elif isinstance(x, ModuleType):
        if hasattr(x,"App"):
            tagClass=getattr(x,"App")
            if not issubclass(tagClass,Tag):
                raise Exception("The 'App' of the module is not inherited from 'htag.Tag class'")
        else:
            raise Exception("module should contains a 'App' (htag.Tag class)")
    elif issubclass(x,Tag):
        tagClass=x
    else:
        raise Exception(f"!!! wtf ({x}) ???")

    return tagClass.__module__+"."+tagClass.__qualname__

parano_seed = lambda uid: hashlib.md5(uid.encode()).hexdigest()

class WebServerSession:  # ASGI Middleware, for starlette
    def __init__(self, app:ASGIApp, https_only:bool = False, sesprovider:"async method(uid)"=None ) -> None:
        self.app = app
        self.session_cookie = "session"
        self.max_age = 0
        self.path = "/"
        self.security_flags = "httponly; samesite=lax"
        if https_only:  # Secure flag can be used with HTTPS only
            self.security_flags += "; secure"
        self.cbsesprovider=sesprovider

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)

        if self.session_cookie in connection.cookies:
            uid = connection.cookies[self.session_cookie]
        else:
            uid = str(uuid.uuid4())

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!
        scope["uid"]     = uid
        scope["session"] = self.cbsesprovider(uid)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!

        logger.debug("request for %s, scope=%s",uid,scope)

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                # send it back, in all cases
                headers = MutableHeaders(scope=message)
                header_value = "{session_cookie}={data}; path={path}; {max_age}{security_flags}".format(  # noqa E501
                    session_cookie=self.session_cookie,
                    data=uid,
                    path=self.path,
                    max_age=f"Max-Age={self.max_age}; " if self.max_age else "",
                    security_flags=self.security_flags,
                )
                headers.append("Set-Cookie", header_value)
            await send(message)

        await self.app(scope, receive, send_wrapper)


def normalize(fqn):
    if ":" not in fqn:
        # replace last "." by ":"
        fqn="".join( reversed("".join(reversed(fqn)).replace(".",":",1)))
    return fqn



class HRSocket(WebSocketEndpoint):
    encoding = "text"

    async def _sendback(self,websocket, txt:str) -> bool:
        try:
            if self.is_parano:
                seed = parano_seed( websocket.scope["uid"])
                txt = crypto.encrypt(txt.encode(),seed)

            await websocket.send_text( txt )
            return True
        except Exception as e:
            logger.error("Can't send to socket, error: %s",e)
            return False

    async def loop_tag_update(self, event, websocket):
        #TODO: there is trouble here sometimes ... to fix !
        with redys.v2.AClient() as bus:
            await bus.subscribe(event)

            ok=True
            while ok:
                actions = await bus.get_event( event )
                if actions is not None:
                    ok=await self._sendback(websocket,json.dumps(actions))
                await asyncio.sleep(0.1)

    async def on_connect(self, websocket):
        #====================================================== get the event
        fqn=websocket.path_params.get("fqn","")
        uid=websocket.scope["uid"]
        event=HrClient(uid,fqn).event_response+"_update"
        #======================================================
        self.is_parano="parano" in websocket.query_params.keys()

        await websocket.accept()

        # add the loop to tag.update feature
        asyncio.ensure_future(self.loop_tag_update(event,websocket))

    async def on_receive(self, websocket, data):
        fqn=websocket.path_params.get("fqn","")
        uid=websocket.scope["uid"]

        if self.is_parano:
            data = crypto.decrypt(data.encode(),parano_seed( uid )).decode()
        data=json.loads(data)

        p=HrClient(uid,fqn)

        actions=await p.interact( oid=data["id"], method_name=data["method"], args=data["args"], kargs=data["kargs"], event=data.get("event") )

        await self._sendback( websocket, json.dumps(actions) )

    async def on_disconnect(self, websocket, close_code):
        #====================================================== get the event
        fqn=websocket.path_params.get("fqn","")
        uid=websocket.scope["uid"]
        event=HrClient(uid,fqn).event_response+"_update"
        #======================================================

        with redys.v2.AClient() as bus:
            await bus.unsubscribe(event)


def processHrServer():
    asyncio.run( redys.v2.loop(hrserver_orchestrator()) )


async def lifespan(app):
    # start a process loop (with redys + hrserver)
    process_hrserver=multiprocessing.Process(target=processHrServer)
    process_hrserver.start()

    # wait hrserver ready
    await wait_hrserver()

    yield

    # stop hrserver
    loop = asyncio.get_event_loop()
    await kill_hrserver()

    # wait process to finnish gracefully
    process_hrserver.join()


class AppServer(Starlette):
    def __init__(self,
                obj:"htag.Tag class|fqn|None"=None,
                session_factory:"sessions.MemDict|sessions.FileDict|sessions.FilePersistentDict|None"=None,
                debug:bool=True,
                ssl:bool=False,
                parano:bool=False,
                http_only:bool=False,
            ):
        self.ssl=ssl
        self.parano = parano
        self.http_only = http_only

        if session_factory is None:
            self.sesprovider = sessions.MemDict
        else:
            self.sesprovider = session_factory

        print("Session with:",self.sesprovider.__name__)
        ###################################################################

        # exposes ws & http routes in all cases
        routes=[
            Route("/_/{fqn}", self.HRHttp, methods=["POST"]),
            WebSocketRoute("/_/{fqn}", HRSocket)
        ]

        #################################################################
        Starlette.__init__( self,
            debug=debug,
            routes=routes,
            middleware=[Middleware(WebServerSession,https_only=ssl,sesprovider=self.sesprovider)],
            lifespan=lifespan,
        )

        if obj:
            async def handleHome(request):
                return await self.handle(request,obj)
            self.add_route( '/', handleHome )

    # new method
    async def handle(self, request,
                    obj:"htag.Tag class|fqn",
                    recreate:bool=False,
                    http_only:"bool|None"=None,
                    parano:"bool|None"=None ) -> HTMLResponse:
        return await self.serve(request,obj,recreate,http_only,parano)


    # DEPRECATED
    async def serve(self, request,
                    obj:"htag.Tag class|fqn",
                    force:bool=False,
                    http_only:"bool|None"=None,
                    parano:"bool|None"=None ) -> HTMLResponse:

        # take default behaviour if not present
        is_parano = self.parano if parano is None else parano
        is_http_only = self.http_only if http_only is None else http_only


        uid = request.scope["uid"]
        args,kargs = commons.url2ak(str(request.url))
        fqn=normalize(findfqn(obj))

        if is_parano:
            seed = parano_seed( uid )

            jslib = crypto.JSCRYPTO
            jslib += f"\nvar _PARANO_='{seed}'\n"
            jslib += "\nasync function _read_(x) {return await decrypt(x,_PARANO_)}\n"
            jslib += "\nasync function _write_(x) {return await encrypt(x,_PARANO_)}\n"
            pparano="?parano"
        else:
            jslib = ""
            jslib += "\nasync function _read_(x) {return x}\n"
            jslib += "\nasync function _write_(x) {return x}\n"
            pparano=""


        if is_http_only:
            # interactions use HTTP POST
            js = """%(jslib)s

            async function interact( o ) {
                let body = await _write_(JSON.stringify(o));
                let req=await window.fetch("/_/%(fqn)s%(pparano)s",{method:"POST", body: body});
                let actions=await req.text();
                action( await _read_(actions) );
            }

            window.addEventListener('DOMContentLoaded', start );
            """ % locals()
        else:
            # interactions use WS
            protocol = "wss" if self.ssl else "ws"

            js = """%(jslib)s

            async function interact( o ) {
                _WS_.send( await _write_(JSON.stringify(o)) );
            }

            // instanciate the WEBSOCKET
            let _WS_=null;
            let retryms=500;

            function connect() {
                _WS_= new WebSocket("%(protocol)s://"+location.host+"/_/%(fqn)s%(pparano)s");
                _WS_.onopen=function(evt) {
                    console.log("** WS connected")
                    document.body.classList.remove("htagoff");
                    retryms=500;
                    start();

                    _WS_.onmessage = async function(e) {
                        let actions = await _read_(e.data)
                        action(actions)
                    };

                }

                _WS_.onclose = function(evt) {
                    console.log("** WS disconnected, retry in (ms):",retryms);
                    document.body.classList.add("htagoff");

                    setTimeout( function() {
                        connect();
                        retryms=retryms*2;
                    }, retryms);
                };
            }
            connect();
            """ % locals()

        p = HrClient(uid,fqn,js,self.sesprovider.__name__,recreate=force)
        html=await p.start(*args,**kargs)
        return HTMLResponse(html)

    async def HRHttp(self,request) -> PlainTextResponse:
        uid = request.scope["uid"]
        fqn = request.path_params.get("fqn","")
        is_parano="parano" in request.query_params.keys()
        seed = parano_seed( uid )

        p=HrClient(uid,fqn)
        data = await request.body()

        if is_parano:
            data = crypto.decrypt(data,seed).decode()

        data=json.loads(data)
        actions=await p.interact( oid=data["id"], method_name=data["method"], args=data["args"], kargs=data["kargs"], event=data.get("event") )
        txt=json.dumps(actions)

        if is_parano:
            txt = crypto.encrypt(txt.encode(),seed)

        return PlainTextResponse(txt)

    def run(self, host="0.0.0.0", port=8000, openBrowser=False):   # localhost, by default !!
        if openBrowser:
            import webbrowser
            webbrowser.open_new_tab(f"http://localhost:{port}")

        uvicorn.run(self, host=host, port=port)
