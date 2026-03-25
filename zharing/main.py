import json

import gevent
import gevent.pywsgi
import uwsgi
import zonzo


@zonzo.query("/status/:op", content_type='application/json')
def status(request_object, op='hola'):
    print(type(request_object))
    return json.dumps({"a": 2, "op": op})


@zonzo.post("/echo", content_type='application/json')
def echo(request, message="hola1"):
    return {"you_said": message}


@zonzo.query("/")
def index(request):
    return "Home Page"


# 1. Main app with no prefix
app_ = zonzo.Application.from_module(__name__)

# # 2. API app with /v1 prefix
# v1_app = Application.from_module("api", prefix="/v1")

# 3. Simple Middleware Dispatcher
# def app(environ, start_response):
#     path = environ.get('PATH_INFO', '')
#     if path.startswith('/v1'):t
#         return v1_app(environ, start_response)
#     return main_app(environ, start_response)


def main():
    print("hola")
    http_server = gevent.pywsgi.WSGIServer(('0.0.0.0', 8000), app_)
    http_server.serve_forever()


import uwsgi


def app(environ, start_response):
    if (
        environ.get("REQUEST_METHOD") == "GET" and
        environ.get("HTTP_UPGRADE", "").lower() == "websocket" and
        "HTTP_SEC_WEBSOCKET_KEY" in environ
        ):
        uwsgi.websocket_handshake(
            environ["HTTP_SEC_WEBSOCKET_KEY"],
            environ.get("HTTP_ORIGIN", "")
            )

        while True:
            chk = uwsgi.websocket_recv()
            uwsgi.websocket_send(chk)
    else:
        start_response(
            "400 Bad Request", [("Content-Type", "text/plain")]
            )
        return [b"Not a WebSocket request"]
