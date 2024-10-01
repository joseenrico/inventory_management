import json
import http.server
import sqlite3
from urllib.parse import urlparse, parse_qs

# Database setup
def init_db():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Handler class
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/items':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            items = get_all_items()
            self.wfile.write(json.dumps(items).encode())
        elif parsed_path.path == '/categories':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            categories = get_all_categories()
            self.wfile.write(json.dumps(categories).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/categories':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            category = json.loads(post_data)
            self.send_response(201)
            self.end_headers()
            add_category(category['name'])
            self.wfile.write(json.dumps({"message": "Category created"}).encode())
        elif parsed_path.path == '/items':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            item = json.loads(post_data)
            self.send_response(201)
            self.end_headers()
            add_item(item['category_id'], item['name'], item.get('description'), item['price'])
            self.wfile.write(json.dumps({"message": "Item created"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

# Database operations
def get_all_items():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT items.id, items.name, items.description, items.price, categories.name AS category FROM items JOIN categories ON items.category_id = categories.id')
    items = cursor.fetchall()
    conn.close()
    return [{"id": item[0], "name": item[1], "description": item[2], "price": item[3], "category": item[4]} for item in items]

def get_all_categories():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    conn.close()
    return [{"id": category[0], "name": category[1]} for category in categories]

def add_category(name):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def add_item(category_id, name, description, price):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (category_id, name, description, price) VALUES (?, ?, ?, ?)',
                   (category_id, name, description, price))
    conn.commit()
    conn.close()

# Server setup
if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MyHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()
