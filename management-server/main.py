import re
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
        "path": "/library/activate",
        "method": "GET",
        "handler": handlers.libraries_handlers.activateLibrary,
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
    {
        "path": "/versions",
        "method": "GET",
        "handler": handlers.system_handlers.getApplicationVersions,
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
        "path": "/library/(?P<id>\\d+)",
        "method": "POST",
        "handler": handlers.libraries_handlers.editLibrary,
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
        "path": "/library_item",
        "method": "DELETE",
        "handler": handlers.library_items_handlers.deleteLibraryItem,
    },
    {
        "path": "/library",
        "method": "DELETE",
        "handler": handlers.libraries_handlers.deleteLibrary,
    },
    {
        "path": "/word",
        "method": "DELETE",
        "handler": handlers.words_handlers.deleteWord,
    },
]


def getRouteHandler(self, method):
    for route in routes:
        if route.get("method") != method:
            continue

        pattern = BASE_ROUTE + str(route.get("path"))
        match = re.match(pattern, self.path)
        if match is None:
            continue

        routeHandler = route.get("handler")
        if routeHandler is None:
            response_utils.InternalServerError(self)
            return None, None

        print(
            "Running handler for",
            route.get("path"),
            "with the match groups ",
            match.groups(),
        )
        # Extract match groups and return them along with the handler

        return routeHandler, match

    response_utils.NotFound(self)
    return None, None


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
        routeHandler, match = getRouteHandler(self, "GET")
        if routeHandler != None:
            query_parameters = None
            if len(self.path.split("?")) > 1:
                query_parameters = parse_qs(self.path.split("?")[1])
            routeHandler(self, query_parameters, match)

    def do_POST(self):
        routeHandler, match = getRouteHandler(self, "POST")
        if routeHandler != None:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            routeHandler(self, post_data, match)

    def do_DELETE(self):
        routeHandler, match = getRouteHandler(self, "DELETE")
        if routeHandler != None:
            query_parameters = None
            if len(self.path.split("?")) > 1:
                query_parameters = parse_qs(self.path.split("?")[1])
            routeHandler(self, query_parameters, match)


# Run the HTTP server
def run():
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on port", port)
    httpd.serve_forever()


if __name__ == "__main__":
    # Call the run function to start the HTTP server
    run()
