import unittest

from app.products import INFO


class TestProducts(unittest.TestCase):

    def test_product_keys(self):
        for elem in INFO:
            for k, v in elem.items():
                if k == "Name":
                    continue
                self.assertIn("_id", v.keys())
                self.assertIn("link", v.keys())
