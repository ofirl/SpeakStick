import json

def okResponse(self):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

def writeJsonResponse(self, data):
    okResponse(self)
    self.wfile.write(json.dumps(data).encode())

def writeTextResponse(self, data: str):
    okResponse(self)
    self.wfile.write(data.encode())

def InternalServerError(self, message: str = "500 internal server error"):
    self.send_response(500)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(message.encode())

def NotFound(self, message: str = "404 Not Found"):
    self.send_response(404)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(message.encode())