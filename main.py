import http.server
import socketserver

# Port to host the server on
PORT = 80

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("looking for "+self.path)
        if self.path == "/":
            self.path = "/pages/home.html"
        elif self.path in ["/element_info", "/compare", "/bohr_models", "/ionic_compound"]:
            self.path = "pages"+self.path+".html"
        elif self.path.startswith("/images") and self.path.endswith(".png"):
            self.path = self.path #image paths should be correct with the GET path
        return super().do_GET()

# Create an HTTP server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving iLearns at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping")
        httpd.server_close()
