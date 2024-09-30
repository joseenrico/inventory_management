import unittest
from handlers import MyHandler

class TestAPI(unittest.TestCase):
    def test_get_categories(self):
        response = MyHandler()._handle_get_categories()
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
