import tornado.ioloop
import tornado.web
import tornado.websocket

from urllib.parse import urlparse


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()

    def check_origin(self, origin):
        return True

    def open(self):
        self.connections.add(self)

    def on_message(self, message):
        self.write_message(message=message)

    def on_close(self):
        self.connections.remove(self)


def make_app():
    return tornado.web.Application([(r"/ws", SimpleWebSocket)])


def startWebSocketServer(port):
    app = make_app()
    print("Starting websocket server on port", port)

    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
