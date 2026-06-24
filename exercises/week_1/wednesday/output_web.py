from http.server import SimpleHTTPRequestHandler, HTTPServer
class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Hello from Python inside Docker and WSL2</h1>")
        self.wfile.write(b"<h2>Output from 'log_processor.py'</h2><p>")
        # Read output.txt into bytes, which can then be written into the page.
        with open("output.txt", "rb") as output:
            self.wfile.write(output.read())
        self.wfile.write(b"<p>")
server = HTTPServer(("0.0.0.0", 8081), MyHandler)
print("Server running on port 8081")
server.serve_forever()