from django.test import TestCase

from django.test import TestCase

class ThincTest(TestCase):
    def test_index(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_no_logic_page(self):
        r = self.client.get('/about/')
        self.assertEqual(r.status_code, 200) 