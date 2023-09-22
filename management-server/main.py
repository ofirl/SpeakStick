import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

import utils.response_utils
import handlers.configs_handlers
import handlers.library_items_handlers
import handlers.libraries_handlers
import handlers.words_handlers
import handlers.system_handlers
import handlers.versions_handlers
import handlers.network_handlers

port = 8090
BASE_ROUTE = "/api"

routes2 = [
    {
        "path": "/configs",
        "routes": [
            {
                "path": "",
                "method": "GET",
                "handler": handlers.configs_handlers.getConfigs,
            },
            {
                "path": "",
                "method": "POST",
                "handler": handlers.configs_handlers.updateConfig,
            },
        ],
    },
    {
        "path": "/libraries",
        "routes": [
            {
                "path": "/(?P<id>.+?)",
                "routes": [
                    {
                        "path": "/activate",
                        "method": "GET",
                        "handler": handlers.libraries_handlers.activateLibrary,
                    },
                    {
                        "path": "/duplicate",
                        "method": "POST",
                        "handler": handlers.libraries_handlers.duplicateLibrary,
                    },
                    {
                        "path": "",
                        "method": "DELETE",
                        "handler": handlers.libraries_handlers.deleteLibrary,
                    },
                    {
                        "path": "",
                        "method": "POST",
                        "handler": handlers.libraries_handlers.editLibrary,
                    },
                ],
            },
            {
                "path": "",
                "method": "POST",
                "handler": handlers.libraries_handlers.addLibrary,
            },
            {
                "path": "",
                "method": "GET",
                "handler": handlers.libraries_handlers.getLibraries,
            },
        ],
    },
    {
        "path": "/library_items",
        "routes": [
            {
                "path": "",
                "method": "DELETE",
                "handler": handlers.library_items_handlers.deleteLibraryItem,
            },
            {
                "path": "",
                "method": "GET",
                "handler": handlers.library_items_handlers.getLibraryItems,
            },
            {
                "path": "",
                "method": "POST",
                "handler": handlers.library_items_handlers.updateLibraryItem,
            },
        ],
    },
    {
        "path": "/network",
        "routes": [
            {
                "path": "/scan",
                "method": "GET",
                "handler": handlers.network_handlers.scanForNetworks,
            },
            {
                "path": "/status",
                "method": "GET",
                "handler": handlers.network_handlers.getNetworkStatus,
            },
            {
                "path": "",
                "method": "POST",
                "handler": handlers.network_handlers.connectToNetwork,
            },
        ],
    },
    {
        "path": "/versions",
        "routes": [
            {
                "path": "/current",
                "method": "GET",
                "handler": handlers.versions_handlers.getApplicationCurrentVersion,
            },
            {
                "path": "/update",
                "method": "GET",
                "handler": handlers.versions_handlers.updateApplicationVersions,
            },
            {
                "path": "/change_log",
                "method": "GET",
                "handler": handlers.versions_handlers.getChageLog,
            },
            {
                "path": "",
                "method": "GET",
                "handler": handlers.versions_handlers.getApplicationVersions,
            },
        ],
    },
    {
        "path": "/words",
        "routes": [
            {
                "path": "",
                "method": "GET",
                "handler": handlers.words_handlers.getWords,
            },
            {
                "path": "",
                "method": "POST",
                "handler": handlers.words_handlers.updateWord,
            },
            {
                "path": "",
                "method": "DELETE",
                "handler": handlers.words_handlers.deleteWord,
            },
        ],
    },
    {
        "path": "/restart/stick-controller",
        "method": "GET",
        "handler": handlers.system_handlers.restartStickController,
    },
    {
        "path": "/upgrade",
        "method": "GET",
        "handler": handlers.versions_handlers.performUpgrade,
    },
    {
        "path": "/reset_factory_settings",
        "method": "GET",
        "handler": handlers.system_handlers.resetToFactorySettings,
    },
]


def getRouteHandler(self, method, baseRoute=BASE_ROUTE, routes=routes2):
    for route in routes:
        route_method = route.get("method", None)
        if route_method is not None and route_method != method:
            continue

        route_path = str(route.get("path"))
        if route_path == "":
            route_path = "/?$"

        pattern = baseRoute + str(route.get("path"))
        requestedPath = self.path.split("?")[0]

        match = re.match(pattern, requestedPath)
        if match is None:
            continue

        routeHandler = route.get("handler", None)
        if routeHandler is None:
            foundHandler, foundMatch = getRouteHandler(
                self, method, pattern, route.get("routes", [])
            )
            if foundHandler is not None:
                return foundHandler, foundMatch

        print(
            "Running handler for ",
            pattern,
            "with the match groups ",
            match.groups(),
        )

        return routeHandler, match

    utils.response_utils.NotFound(self)
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
        if routeHandler is not None:
            query_parameters = None
            if len(self.path.split("?")) > 1:
                query_parameters = parse_qs(self.path.split("?")[1])
            routeHandler(self, query_parameters, match)

    def do_POST(self):
        routeHandler, match = getRouteHandler(self, "POST")
        if routeHandler is not None:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            routeHandler(self, post_data, match)

    def do_DELETE(self):
        routeHandler, match = getRouteHandler(self, "DELETE")
        if routeHandler is not None:
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
