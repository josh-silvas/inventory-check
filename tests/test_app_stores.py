import unittest

from app.store import Amazon, WalMart, BestBuy, NewEgg, Target
from app.config import Config
from app.products import INFO


class TestStores(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        cfg = Config("app/config-example.ini")
        self.amazon = Amazon(INFO[0], cfg)
        self.best_buy = BestBuy(INFO[0], cfg)
        self.new_egg = NewEgg(INFO[0], cfg)
        self.target = Target(INFO[0], cfg)
        self.walmart = WalMart(INFO[0], cfg)
        super(TestStores, self).__init__(*args, **kwargs)

    def test_amazon_check_availability(self):
        with open("tests/mock/01-mock.html", "r") as _file:
            ans = self.amazon.fetch(_file.read())
            self.assertIsNotNone(ans)
            self.assertRegex(
                ans,
                r"(only\s+\d+\s+left\s+in\s+stock|currently\s+unavailable|in\s+stock)",
            )

    def test_walmart_check_availability(self):
        with open("tests/mock/02-mock.html", "r") as _file:
            ans = self.walmart.fetch(_file.read())
            self.assertIsNotNone(ans)
            self.assertEqual(ans, "add to cart")
