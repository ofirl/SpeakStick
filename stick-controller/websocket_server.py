import time

import logging
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
                logging.debug(f"connection is already closed")
                self.running = False
                return

            time.sleep(0.2)

    def on_message(self, message):
        self.write_message(message=message)

    def on_close(self):
        self.running = False
        logging.debug("connection closed")


def make_app():
    return tornado.web.Application([(r"/ws/stick-position", SimpleWebSocket)])


def startWebSocketServer(port):
    app = make_app()
    logging.info(f"Starting websocket server on {port}")

    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
