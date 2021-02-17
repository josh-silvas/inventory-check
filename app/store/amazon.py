from lxml import html
from app.util import success, info
import requests


class Amazon:
    def __init__(self, product_info, cfg):
        self.cfg = cfg
        self.store_name = self.__class__.__name__
        self.product_id = product_info.get(self.store_name).get("_id")
        self.product_link = product_info.get(self.store_name).get("link")
        self.product_name = product_info.get("Name")

    def check_availability(self) -> bool:
        if self.product_link is None:
            return False
        page = requests.get(
            url=self.product_link,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
                "Referer": "http://www.amazon.com/dp/",
                "Accept": "application/json",
            },
        )
        ans = self.fetch(page.content)
        if ans in "In Stock.".lower():
            success(f"[{self.store_name}] {self.product_name} Available!")
            return True

        if ans in "Only 2 left in stock.".lower():
            success(f"[{self.store_name}] {self.product_name} Available!")
            return True

        if ans in "Only 1 left in stock.".lower():
            success(f"[{self.store_name}] {self.product_name} Available!")
            return True

        info(f"[{self.store_name}] {self.product_name} not available")
        return False

    @staticmethod
    def fetch(content) -> [str, None]:
        doc = html.fromstring(content)
        # checking availability
        xpath_availability = '//div[@id ="availability"]//text()'
        raw_availability = doc.xpath(xpath_availability)
        return (
            str("".join(raw_availability).strip().rstrip()).lower()
            if raw_availability
            else None
        )
