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
        time.sleep(1)
        while self.running:
            messageFuture = self.write_message(str(globals.current_cell))
            while not messageFuture.done:
                time.sleep(0.1)
            if messageFuture.exception is not None:
                print(f"closing connection {messageFuture.exception}")
                self.running = False
                self.close()
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
