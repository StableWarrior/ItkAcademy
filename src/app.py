from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        message = f"Hello from LMS! 👋\nPath: {self.path}\n"
        self.wfile.write(message.encode())

port = int(os.getenv('PORT', 8000))
server = HTTPServer(('', port), Handler)
print(f'Server started on port {port}')
server.serve_forever()

