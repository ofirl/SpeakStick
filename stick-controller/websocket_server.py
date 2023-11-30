import time

# import threading
import tornado.ioloop
import tornado.web
import tornado.websocket

from urllib.parse import urlparse

import globals


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.running = True
        time.sleep(2)
        while self.running:
            try:
                messageFuture = self.write_message(str(globals.current_cell))
                while not messageFuture.done:
                    time.sleep(0.1)
            except tornado.websocket.WebSocketClosedError as e:
                print(f"connection is already closed")
                return

            time.sleep(0.5)

    def on_message(self, message):
        self.write_message(message=message)

    def on_close(self):
        self.running = False
        print("connection closed")


def make_app():
    return tornado.web.Application([(r"/ws/stick-position", SimpleWebSocket)])


def startWebSocketServer(port):
    app = make_app()
    print("Starting websocket server on port", port)

    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
