from server import app
import unittest


class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
    
    # executed after each test
    def tearDown(self):
        pass
 
    def test_resize_route(self):
        response = self.app.get('/resize?url=https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg&size=500x500', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 
    def test_root_route(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
