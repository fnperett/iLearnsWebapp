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
        elif self.path == "/settings":
            self.path = "/pages/settings.html"
        elif self.path.startswith("/tag-info"):
            info = self.path[len("/tag-info/"):]
            response = mongo.getTagInfo(info, mongo.tags)
            if not response:
                response = {"Error": "Tag not found"}
            elif response["Element"] == "yes":
                element = response["Tag Name"].capitalize()
                response = mongo.getElementInfo(element, mongo.elements)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")  # Content-Type
            self.send_header("Content-Length", str(len))
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
            return
        elif self.path.startswith("/update-tag"):
            tag_info = self.path[len("/update-tag/"):].split("/")
            if len(tag_info) == 2:
                tag_name = tag_info[0]
                tag_id = tag_info[1]
                mongo.updateTag(tag_name, tag_id, mongo.tags)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Tag updated successfully")
                return
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid update request")
                return
        
        return super().do_GET()
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))  # Get the content length
        post_data = self.rfile.read(content_length)  # Read the POST data

        try:
            data = json.loads(post_data.decode('utf-8'))  # Parse JSON data
            print("Received POST data:", data)

            if(data.get("button_remap", None) != None):
                response = {"status": "success", "message": "Button "+data.get("button_remap")+" was re-mapped"}
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                # Example response
                response = {"status": "unknown", "message": "unknown path"}
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
        
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "Invalid JSON"}).encode('utf-8'))

# Create an HTTP server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving iLearns at http://localhost:{PORT}")
    mongo.csvToCollection("./csv/element_database.csv",mongo.elements)
    mongo.csvToCollection("./csv/tag_database.csv",mongo.tags)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping")
        httpd.server_close()

