from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

import response_utils
import handlers.configs_handlers
import handlers.library_items_handlers
import handlers.libraries_handlers
import handlers.words_handlers
import handlers.system_handlers

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
        "path": "/libraries",
        "method": "GET",
        "handler": handlers.libraries_handlers.getLibraries,
    },
    {
        "path": "/library_items",
        "method": "GET",
        "handler": handlers.library_items_handlers.getLibraryItems,
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
        "path": "/library/duplicate",
        "method": "POST",
        "handler": handlers.libraries_handlers.duplicateLibrary,
    },
    {
        "path": "/library_item",
        "method": "POST",
        "handler": handlers.library_items_handlers.updateLibraryItem,
    },
    {
        "path": "/library",
        "method": "POST",
        "handler": handlers.libraries_handlers.addLibrary,
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
        "path": "/library",
        "method": "DELETE",
        "handler": handlers.libraries_handlers.deleteLibrary,
    },
    {
        "path": "/library_item",
        "method": "DELETE",
        "handler": handlers.library_items_handlers.deleteLibraryItem,
    },
    {
        "path": "/word",
        "method": "DELETE",
        "handler": handlers.words_handlers.deleteWord,
    },
]

def getRouteHandler(self, method):
    route = next((route for route in routes if route.get("method") == method and \
            ( \
                self.path.startswith(BASE_ROUTE + str(route.get("path"))) \
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
            query_parameters = None
            if len(self.path.split('?')) > 1:
                query_parameters = parse_qs(self.path.split('?')[1])
            routeHandler(self, query_parameters)

    def do_POST(self):
        routeHandler = getRouteHandler(self, "POST")
        if routeHandler != None:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            routeHandler(self, post_data)

    def do_DELETE(self):
        routeHandler = getRouteHandler(self, "DELETE")
        if routeHandler != None:
            query_parameters = None
            if len(self.path.split('?')) > 1:
                query_parameters = parse_qs(self.path.split('?')[1])
            routeHandler(self, query_parameters)

# Run the HTTP server
def run():
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on port", port)
    httpd.serve_forever()

if __name__ == "__main__":
    # Call the run function to start the HTTP server
    run()