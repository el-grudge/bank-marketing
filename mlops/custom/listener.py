from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length)  # Read the POST data

        # Parse the JSON data
        data = json.loads(post_data)

        # Get title and message from the parsed data
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        title = data.get('title', 'No Title')
        message = data.get('message', 'No Message')

        # Define the path where the dummy file will be created
        file_path = f"mlops/payloads/alert_{now}.txt"
        
        # Create a dummy text file with the title and message
        with open(file_path, 'w') as f:
            f.write(f"Title: {title}\nMessage: {message}\n")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Alert received and file created.')


@custom
def transform_custom(*args, **kwargs):
    server_address = ('0.0.0.0', 6790)  # Server listening on port 6790
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Running webhook listener on port 6790...')
    httpd.serve_forever()
