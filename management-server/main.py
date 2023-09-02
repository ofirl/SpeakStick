from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import parse_qs
import json

import db_utils

import response_utils
import handlers.configs_handlers
import handlers.positions_handlers
import handlers.words_handlers
import handlers.system_handlers

from consts import words_directory

port = 8090
BASE_ROUTE = "/api"

routes = [
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
]

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
        route = next((route for route in routes if route.get("method") == "GET" and self.path == BASE_ROUTE + str(route.get("path"))), None)
        if route == None:
            response_utils.NotFound(self)
        else:
            routeHandler = route.get("handler")
            if routeHandler == None:
                response_utils.NotFound(self)
            else:
                print("calling a route handler")
                routeHandler(self)

        print("call end headers")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == BASE_ROUTE + "/config":
            json_data = json.loads(post_data.decode('utf-8'))
            key = json_data.get('key')
            value = json_data.get('value')
            success = db_utils.update_config(key, value)
            if success:
                self.send_response(200)
            else:
                self.send_response(500)
            self.end_headers()
            
        elif self.path == BASE_ROUTE + "/position":
            json_data = json.loads(post_data.decode('utf-8'))
            position = json_data.get('position')
            new_word = json_data.get('word')
            success = db_utils.update_position(position, new_word)
            if success:
                self.send_response(200)
            else:
                self.send_response(500)
            self.end_headers()

        elif self.path == BASE_ROUTE + "/word":
            # Read the uploaded file and save it
            file_name = self.headers.get('filename', '')
            if file_name == "":
                self.send_response(400)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Mssing 'filename' header")
                return

            file_path = os.path.join(words_directory, file_name)

            with open(file_path, 'wb') as f:
                f.write(post_data)

            self.send_response(200)  # OK
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            response = f"File '{file_name}' uploaded successfully"
            self.wfile.write(response.encode())
        
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_DELETE(self):
        if self.path.startswith(BASE_ROUTE + "/position"):
            query_parameters = parse_qs(self.path.split('?')[1])
            position = query_parameters.get('position')
            
            success = db_utils.delete_position(position)
            if success:
                self.send_response(200)
            else:
                self.send_response(500)
            self.end_headers()
        
        if self.path.startswith(BASE_ROUTE + "/word"):
            query_parameters = parse_qs(self.path.split('?')[1])
            word = query_parameters.get('word')
            if not word:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"400 Bad Request - word parameter expected")
                return

            error = db_utils.delete_word("".join(word))
            if error == None:
                self.send_response(200)
            else:
                self.send_response(500)
                self.wfile.write(error.__str__().encode())
            self.end_headers()
        
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

# Run the HTTP server
def run():
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on port", port)
    httpd.serve_forever()

if __name__ == "__main__":
    # Call the run function to start the HTTP server
    run()