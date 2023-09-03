from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

import response_utils
import handlers.configs_handlers
import handlers.positions_handlers
import handlers.words_handlers
import handlers.system_handlers

import system_utils

port = 8090
BASE_ROUTE = "/api"

routes = [
    # GET --- GET --- GET --- GET --- GET --- GET --- GET --- GET --- GET ---
    {
        "path": "/configs",
        "method": "GET",
        "handler": handlers.configs_handlers.getConfigs,
    },
    {
        "path": "/positions",
        "method": "GET",
        "handler": handlers.positions_handlers.getPositions,
    },
    {
        "path": "/words",
        "method": "GET",
        "handler": handlers.words_handlers.getWords,
    },
    {
        "path": "/restart/stick-controller",
        "method": "GET",
        "handler": handlers.system_handlers.restartStickController,
    },
    {
        "path": "/upgrade",
        "method": "GET",
        "handler": handlers.system_handlers.performUpgrade,
    },
    {
        "path": "/network/scan",
        "method": "GET",
        "handler": handlers.system_handlers.scanForNetworks,
    },
    {
        "path": "/network/status",
        "method": "GET",
        "handler": handlers.system_handlers.getNetworkStatus,
    },
    # POST --- POST --- POST --- POST --- POST --- POST --- POST --- POST ---
    {
        "path": "/config",
        "method": "POST",
        "handler": handlers.configs_handlers.updateConfig,
    },
    {
        "path": "/position",
        "method": "POST",
        "handler": handlers.positions_handlers.updatePosition,
    },
    {
        "path": "/word",
        "method": "POST",
        "handler": handlers.words_handlers.updateWord,
    },
    {
        "path": "/network/update",
        "method": "POST",
        "handler": handlers.system_handlers.connectToNetwork,
    },
    # DELETE --- DELETE --- DELETE --- DELETE --- DELETE --- DELETE --- DELETE ---
    {
        "path": "/position",
        "method": "DELETE",
        "handler": handlers.positions_handlers.deletePosition,
    },
    {
        "path": "/word",
        "method": "DELETE",
        "handler": handlers.words_handlers.deleteWord,
    },
]

def getRouteHandler(self, method, startsWith = False):
    route = next((route for route in routes if route.get("method") == method and \
            ( \
                (startsWith and self.path.startswith(BASE_ROUTE + str(route.get("path")))) or \
                self.path == BASE_ROUTE + str(route.get("path")) \
            ) \
        ), None)
    if route == None:
        response_utils.NotFound(self)
    else:
        routeHandler = route.get("handler")
        if routeHandler == None:
            response_utils.NotFound(self)
        else:
            return routeHandler
        
    return None

# Define the HTTP request handler class
class RequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        BaseHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Headers", "filename")
        self.end_headers()

    def do_GET(self):
        routeHandler = getRouteHandler(self, "GET")
        if routeHandler != None:
            routeHandler(self)

    def do_POST(self):
        routeHandler = getRouteHandler(self, "POST")
        if routeHandler != None:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            routeHandler(self, post_data)

    def do_DELETE(self):
        routeHandler = getRouteHandler(self, "DELETE", True)
        if routeHandler != None:
            routeHandler(self)

# Run the HTTP server
def run():
    # system_utils.runCommand("sleep 30")
    # system_utils.restartNetworkServices()
    # system_utils.runCommand("sleep 10")

    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on port", port)
    httpd.serve_forever()

if __name__ == "__main__":
    # Call the run function to start the HTTP server
    run()