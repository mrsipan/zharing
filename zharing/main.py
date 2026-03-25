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

import time

import gevent

TICK_RATE = 20
TICK_DT = 1.0 / TICK_RATE

Tick_global = 0


def tick_loop():
    global Tick_global
    tick_next = time.monotonic()

    while True:
        time_real = time.monotonic()

        if time_real < tick_next:
            gevent.sleep(tick_next - time_real)

        Tick_global += 1
        step_simulation(tick)
        tick_next += TICK_DT


gevent.spawn(tick_loop)

import collections

dq_clients = collections.defaultdict(collections.deque)


def handle_client_message(id_player, msg):
    if msg['type'] == 'input':
        dq_clients[id_player].append(msg)


def sumulation_step(tick):
    collect_inputs_from_clients()
    update_world()
    send_state_updates(tick)


def collect_inputs():
    for id_player, qu in dq_clients.items():
        while qu:
            msg_input = qu.popleft()
            apply_input(id_player, msg_input)


def send_state_updates(tick):
    delta = compute_state_delta()

    msg = {
        'type': 'state_delta',
        'tick': tick,
        'payload': delta,
        }

    msg_encoded = json.dumps(msg)

    for ws in clients:
        ws.send(msg_encoded)


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
