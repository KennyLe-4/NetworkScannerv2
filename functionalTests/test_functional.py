import unittest
from app import app  # Importing the Flask app

class FlaskAppTests(unittest.TestCase):
       def setUp(self):
           self.app = app.test_client()  # Create a test client
           self.app.testing = True

       def test_home_page_loads(self):
           response = self.app.get('/')
           self.assertEqual(response.status_code, 200)  # Check if the home page loads

       def test_scan_redirect(self):
           response = self.app.post('/', data={'target': '192.168.1.1', 'scan_type': 'vuln'})
           self.assertEqual(response.status_code, 302)  # Check for redirect to scan results

       def test_invalid_ip(self):
        response = self.app.post('/', data={'target': 'invalid_ip', 'scan_type': 'vuln'})
        self.assertIn(b'Invalid IP address', response.data)  # Check for error message
        
        if __name__ == '__main__':
              unittest.main()
       