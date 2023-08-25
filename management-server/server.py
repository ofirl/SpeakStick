from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json

import db

port = 8080

# Define the HTTP request handler class
class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/configs":
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
            
        elif self.path == "/words":
            words = db.get_words()
            if words:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(words).encode())
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
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)
        
        if self.path == "/config":
            key = parsed_data.get('key', [''])[0]
            value = parsed_data.get('value', [''])[0]
            success = db.update_config(key, value)
            if success:
                self.send_response(200)
            else:
                self.send_response(500)
            self.end_headers()
            
        elif self.path == "/word":
            position = parsed_data.get('position', [''])[0]
            new_word = parsed_data.get('word', [''])[0]
            success = db.update_word(position, new_word)
            if success:
                self.send_response(200)
            else:
                self.send_response(500)
            self.end_headers()

# Run the HTTP server
def run():
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on port", port)
    httpd.serve_forever()

# Call the run function to start the HTTP server
run()
