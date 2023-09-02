import system_utils

def restartStickController(self):
    return_code, _ = system_utils.restartStickController()
    if return_code == 0:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
    else:
        self.send_response(500)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"500 internal server error")