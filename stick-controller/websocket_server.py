import time

# import threading
import tornado.ioloop
import tornado.web
import tornado.websocket

from urllib.parse import urlparse

from main import getCurrentCell


# def sendPositions(websocket):
#     while websocket.running:
#         websocket.write_message(str(current_cell))
#         time.sleep(0.1)


class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.running = True
        time.sleep(1)
        while self.running:
            current_cell = str(getCurrentCell())
            print(f"current_cell: {current_cell}")
            self.write_message(current_cell)
            time.sleep(0.5)
        # websocketServerThread = threading.Thread(target=sendPositions, args=(self,))
        # websocketServerThread.start()

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
