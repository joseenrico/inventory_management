from http.server import HTTPServer
from handlers import MyHandler
from models import setup_db

def run():
    setup_db()  # Setup database
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("Server berjalan pada port 8000...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
