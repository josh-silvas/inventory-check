import unittest
import json

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

    def test_best_buy_in_store_availability(self):
        with open("tests/mock/05-mock.json", "r") as _file:
            resp = self.best_buy.check_within_zip_inventory(json.loads(_file.read()))
            self.assertEqual(resp, ["Bucktown"])

    def test_best_buy_online_availability(self):
        with open("tests/mock/06-mock.json", "r") as _file:
            resp = self.best_buy.check_online_inventory(json.loads(_file.read()))
            self.assertEqual(resp, ["Online"])

    def test_walmart_check_availability(self):
        with open("tests/mock/02-mock.html", "r") as _file:
            ans = self.walmart.check_inventory(_file.read())
            self.assertIsNotNone(ans)
            self.assertEqual(ans, "add to cart")

    def test_target_check_availability(self):
        with open("tests/mock/03-mock.json", "r") as _file:
            resp = self.target.check_for_inventory(json.loads(_file.read()))
            self.assertEqual(resp[1], "out of stock online and in stores")

    def test_new_egg_check_availability(self):
        with open("tests/mock/04-mock.html", "r") as _file:
            resp = self.new_egg.check_for_inventory(_file.read())
            self.assertTrue(resp)
