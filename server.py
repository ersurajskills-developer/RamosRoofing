import http.server
import socketserver
import os
import urllib.parse

PORT = 8080

class DevServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse URL path
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Apply Netlify redirects/rewrites (from netlify.toml)
        redirects = {
            '/about': '/about.html',
            '/before-after': '/before-after.html',
            '/reviews': '/reviews.html'
        }
        
        if path in redirects:
            # Internally rewrite the path to the HTML file (status 200)
            self.path = redirects[path] + ('?' + parsed_url.query if parsed_url.query else '')
            print(f"Rewrite: {path} -> {self.path}")
            
        return super().do_GET()

if __name__ == '__main__':
    # Change working directory to the script's directory to serve files correctly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DevServerHandler) as httpd:
        print(f"Serving local site at: http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server.")
