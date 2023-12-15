import time
import threading
import logging
import tornado.ioloop
import tornado.web
import tornado.websocket
import asyncio


import globals

connections = []


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        connections.append((self, self.write_message))

    def on_message(self, message):
        if message != "keep-alive":
            self.write_message(message=message)

    def on_close(self):
        if connections.__contains__(self):
            connections.remove(self)
        logging.debug("connection closed")


def make_app():
    return tornado.web.Application([(r"/ws/stick-position", SimpleWebSocket)])


def handle_websocket_connections():
    logging.debug("stick events websocket handler started")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        stickEvent = globals.stick_events.get()
        logging.debug("handling event", extra={"event": stickEvent})
        for connection, write_message in connections:
            try:
                messageFuture = write_message(stickEvent)
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
    # asyncio.run(handle_websocket_connections())

    app = make_app()
    logging.info(f"Starting websocket server on {port}")

    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
