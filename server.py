from http.server import SimpleHTTPRequestHandler, HTTPServer
import json

# Global state to track if the payload ran
payload_executed = False

class C2Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        global payload_executed
        
        # 1. The .bat file hits this endpoint when clicked
        if self.path == '/beacon':
            payload_executed = True
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Beacon received")
            print("\n[+] PAYLOAD EXECUTED: Beacon received from .vbs file!\n")
            return
            
        # 2. The webpage constantly checks this endpoint
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"executed": payload_executed}
            self.wfile.write(json.dumps(response).encode())
            return
            
        # Serve the index.html
        return super().do_GET()

print("Hosting survey PoC on http://localhost:8000")
HTTPServer(('localhost', 8000), C2Handler).serve_forever()