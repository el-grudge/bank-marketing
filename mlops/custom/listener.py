from http.server import BaseHTTPRequestHandler, HTTPServer
import os

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Define the path where the dummy file will be created
        file_path = "/path/to/dummy_file.txt"
        
        # Create a dummy text file
        with open(file_path, 'w') as f:
            f.write("Alert received from Grafana")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Alert received and file created.')


@custom
def transform_custom(*args, **kwargs):
    server_address = ('', 6790)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Running webhook listener on port 6789...')
    httpd.serve_forever()

