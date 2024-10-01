import unittest
import requests

class TestInventoryAPI(unittest.TestCase):
    BASE_URL = 'http://localhost:8000'

    def test_get_items(self):
        response = requests.get(f'{self.BASE_URL}/items')
        self.assertEqual(response.status_code, 200)

    def test_get_categories(self):
        response = requests.get(f'{self.BASE_URL}/categories')
        self.assertEqual(response.status_code, 200)

    def test_add_category(self):
        response = requests.post(f'{self.BASE_URL}/categories', json={"name": "Python"})
        self.assertEqual(response.status_code, 201)

    def test_add_item(self):
        response = requests.post(f'{self.BASE_URL}/items', json={"category_id": 1, "name": "New Item", "price": 10.0})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
