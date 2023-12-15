import time
import threading
import logging
import tornado.ioloop
import tornado.web
import tornado.websocket


import globals

connections = []


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        connections.append(self)

    def on_message(self, message):
        self.write_message(message=message)

    def on_close(self):
        connections.remove(self)
        logging.debug("connection closed")


def make_app():
    return tornado.web.Application([(r"/ws/stick-position", SimpleWebSocket)])


def handle_websocket_connections():
    logging.debug("stick events websocket handler started")

    while True:
        stickEvent = globals.stick_events.get()
        logging.debug("handling event", extra={"event": stickEvent})
        for connection in connections:
            try:
                messageFuture = connection.write_message(stickEvent)
                while not messageFuture.done:
                    time.sleep(0.1)
            except tornado.websocket.WebSocketClosedError as e:
                logging.debug(f"connection is already closed")
            except Exception as e:
                logging.exception(
                    "Error sending message", extra={"message": stickEvent}
                )


def startWebSocketServer(port):
    webscoketConnectionHandler = threading.Thread(
        target=handle_websocket_connections, args=()
    )
    webscoketConnectionHandler.start()

    app = make_app()
    logging.info(f"Starting websocket server on {port}")

    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
