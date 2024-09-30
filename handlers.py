import json
from http.server import BaseHTTPRequestHandler
from models import connect_db

# Handler request HTTP
class MyHandler(BaseHTTPRequestHandler):
    def _send_response(self, code, content):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(content).encode())

    def do_GET(self):
        if self.path == '/categories':
            self._handle_get_categories()
        elif self.path == '/items':
            self._handle_get_items()
        else:
            self._send_response(404, {"error": "Endpoint tidak ditemukan"})

    def _handle_get_categories(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Category')
        categories = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        self._send_response(200, categories)
        conn.close()

    def _handle_get_items(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Item.id, Item.name, Item.description, Item.price, Category.name AS category
            FROM Item JOIN Category ON Item.category_id = Category.id
        ''')
        items = [{"id": row[0], "name": row[1], "description": row[2], "price": row[3], "category": row[4]} for row in cursor.fetchall()]
        self._send_response(200, items)
        conn.close()

    def do_POST(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass
