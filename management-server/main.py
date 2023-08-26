from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.parse import parse_qs
import json

import db
import system

from consts import words_directory

port = 8090
BASE_ROUTE = "/api"

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
        self.end_headers()

    def do_GET(self):
        if self.path == BASE_ROUTE + "/configs":
            configs = db.get_configs()
            if configs:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(configs).encode())
            else:
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"500 internal server error")
            
        elif self.path == BASE_ROUTE + "/positions":
            files = db.get_positions()
            if files:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(files).encode())
            else:
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"500 internal server error")
        
        elif self.path == BASE_ROUTE + "/words":
            files = system.getWordFiles()
            if files:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(files).encode())
            else:
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"500 internal server error")

        elif self.path == BASE_ROUTE + "/restart/stick-controller":
            return_code, _ = system.restartStickController()
            if return_code == 0:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
            else:
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"500 internal server error")
            
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == BASE_ROUTE + "/config":
            json_data = json.loads(post_data.decode('utf-8'))
            key = json_data.get('key')
            value = json_data.get('value')
            success = db.update_config(key, value)
            if success:
                self.send_response(200)
            else:
                self.send_response(500)
            self.end_headers()
            
        elif self.path == BASE_ROUTE + "/position":
            json_data = json.loads(post_data.decode('utf-8'))
            position = json_data.get('position')
            new_word = json_data.get('word')
            success = db.update_position(position, new_word)
            if success:
                self.send_response(200)
            else:
                self.send_response(500)
            self.end_headers()

        elif self.path == BASE_ROUTE + "/word":
            content_type = self.headers['Content-Type']

            if "multipart/form-data" in content_type:
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
                self.send_response(400)  # Bad Request
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                response = "Invalid content type"
                self.wfile.write(response.encode())

        # elif self.path == BASE_ROUTE + "/word":
        #     content_length = int(self.headers['Content-Length'])
        #     uploaded_file = self.rfile.read(content_length)

        #     filename = self.headers.get('filename', '')
        #     if filename == "":
        #         self.send_response(400)
        #         self.send_header("Content-type", "text/plain")
        #         self.end_headers()
        #         self.wfile.write(b"Mssing 'filename' header")

        #     filepath = os.path.join(words_directory, filename)

        #     with open(filepath, 'wb') as f:
        #         f.write(uploaded_file)

        #     self.send_response(200)
        #     self.send_header("Content-type", "text/plain")
        #     self.end_headers()
        #     self.wfile.write(b"File uploaded successfully.")
        
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_DELETE(self):
        if self.path.startswith(BASE_ROUTE + "/position"):
            query_parameters = parse_qs(self.path.split('?')[1])
            position = query_parameters.get('position')
            
            success = db.delete_position(position)
            if success:
                self.send_response(200)
            else:
                self.send_response(500)
            self.end_headers()
        
        if self.path.startswith(BASE_ROUTE + "/word"):
            query_parameters = parse_qs(self.path.split('?')[1])
            word = query_parameters.get('word')
            
            msg, error = db.delete_word(word)
            if error == None:
                self.send_response(200)
            else:
                self.send_response(500)
                self.wfile.write(msg)
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