import requests

from lxml import html
from typing import Dict
from app.util.log import success, info


class WalMart:
    def __init__(self, product_info: Dict, cfg):
        self.cfg = cfg
        self.store_name = self.__class__.__name__
        self.product_id = product_info.get(self.store_name).get("_id")
        self.product_link = product_info.get(self.store_name).get("link")
        self.product_name = product_info.get("Name")

    def check_availability(self) -> bool:
        if self.product_link is None:
            return False
        r = requests.get(
            url=self.product_link,
            headers={
                "Accept": "application/json",
                "Referer": "https://www.walmart.com/",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
            },
        )
        ans = self.check_inventory(r.content)
        if not ans:
            return False
        if ans in "add to cart":
            success(f"[{self.store_name}] {self.product_name} Available!")
            return True

        info(f"[{self.store_name}] {self.product_name} not available")
        return False

    @staticmethod
    def check_inventory(content):
        doc = html.fromstring(content)
        raw_availability = doc.xpath(
            '//*[contains(@class, "prod-ProductCTA--primary")]//text()'
        )
        return (
            str("".join(raw_availability).strip()).lower() if raw_availability else None
        )
