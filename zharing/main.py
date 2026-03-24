import json

import gevent
import gevent.pywsgi
import zonzo


@zonzo.query("/status/:op", content_type='application/json')
def status(request_object, op='hola'):
    print(type(request_object))
    return json.dumps({"a": 2, "op": op})


@zonzo.post("/echo")
def echo(request, message):
    return {"you_said": message}


@zonzo.query("/")
def index(request):
    return "Home Page"


# 1. Main app with no prefix
app = zonzo.Application.from_module(__name__)

# # 2. API app with /v1 prefix
# v1_app = Application.from_module("api", prefix="/v1")

# 3. Simple Middleware Dispatcher
# def app(environ, start_response):
#     path = environ.get('PATH_INFO', '')
#     if path.startswith('/v1'):
#         return v1_app(environ, start_response)
#     return main_app(environ, start_response)


def main():
    print("hola")
    http_server = gevent.pywsgi.WSGIServer(('0.0.0.0', 8000), app)
    http_server.serve_forever()
