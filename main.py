import http.server
import socketserver
import mongo
import json

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
        elif self.path.startswith("/compare-info"):
            info = self.path[len("/compare-info/"):]  # Get the part after "/compare-info/"
            response = mongo.getElementInfo(info, mongo.elements)
            self.send_response(200)  # HTTP status code 200 (OK)
            self.send_header("Content-Type", "application/json")  # Content-Type
            self.send_header("Content-Length", str(len))
            self.end_headers()

            # Convert the dictionary to a JSON string and write it as the response
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        elif self.path.startswith("/element-info"):
            info = self.path[len("/element-info/"):]  # Get the part after "/compare-info/"
            response = mongo.getElementInfo(info, mongo.elements)
            self.send_response(200)  # HTTP status code 200 (OK)
            self.send_header("Content-Type", "application/json")  # Content-Type
            self.send_header("Content-Length", str(len))
            self.end_headers()

            # Convert the dictionary to a JSON string and write it as the response
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        return super().do_GET()

# Create an HTTP server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving iLearns at http://localhost:{PORT}")
    mongo.csvToCollection("./csv/element_database.csv",mongo.elements)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping")
        httpd.server_close()
