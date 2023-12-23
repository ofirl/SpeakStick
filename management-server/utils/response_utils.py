import json

def okResponse(self):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()

def okWithData(self, data):
    okResponse(self)
    self.wfile.write(json.dumps(data).encode())

def okWithText(self, data: str):
    okResponse(self)
    self.wfile.write(data.encode())

def okWithFile(self, filename, data):
    okResponse(self)
    self.send_header('Content-Type', 'application/zip')
    self.send_header('Content-Disposition', 'attachment; filename={filename}'.format(filename=filename))
    self.send_header('Content-Length', len(data))
    self.end_headers()
    self.wfile.write(data)
    
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

def BadRequest(self, message: str = "400 Bad Request"):
    self.send_response(400)
    self.send_header("Content-type", "text/plain")
    self.end_headers()
    self.wfile.write(message.encode())