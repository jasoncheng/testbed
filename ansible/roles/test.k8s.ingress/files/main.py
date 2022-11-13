from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes('<html><head><title>Hello</title></head><body>', 'utf-8'))
        self.wfile.write(bytes("<h2>Host %s</h2>" % self.headers.get('Host'), 'utf-8'))
        self.wfile.write(bytes("<h2>Path %s</h2>" % self.path, 'utf-8'))
        self.wfile.write(bytes("<h2>PodName %s</h2>" % os.getenv('POD_NAME'), 'utf-8'))
        self.wfile.write(bytes("<h2>PodIP %s</h2>" % os.getenv('POD_IP'), 'utf-8'))
        self.wfile.write(bytes('</body></html>', "utf-8"))
        
if __name__ == "__main__":
    webServer = HTTPServer(("localhost", 8087), WebServer)
    try:
        webServer.serve_forever()
        print("Server running....")
    except:
        pass
    
    webServer.server_close()
    print("Server stopped.")