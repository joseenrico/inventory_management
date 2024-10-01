# debug/main.py
import json
import http.server

def get_all_items():
     return {"items": [{"name": "Python"}, {"name": "Python 2"}]}

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/items':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            items = get_all_items()
            self.wfile.write(json.dumps(items).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    print('Starting server...')
    httpd.serve_forever()
