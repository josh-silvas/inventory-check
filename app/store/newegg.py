import time
import requests
from lxml import html
from typing import Dict
from util.log import success, info


class NewEgg:

    def __init__(self, product_info: Dict, cfg):
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
                "Referer": "https://www.newegg.com/",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
            },
        )
        doc = html.fromstring(page.content)
        try:
            raw_availability = doc.xpath(
                '//div[@id ="ProductBuy"]//span[contains(@class, "btn-message")]//text()'
            )
            result = "".join(raw_availability).strip() if raw_availability else None
            if str(result) in str("Sold Out"):
                info(f"[{self.store_name}] {self.product_name} not available")
                return False

            raw_availability = doc.xpath(
                '//div[contains(@class, "flags-body")]//text()'
            )
            result = "".join(raw_availability).strip() if raw_availability else None
            if str(result) in str("CURRENTLY SOLD OUT"):
                info(f"[{self.store_name}] {self.product_name} not available")
                return False
        except:
            time.sleep(1)

        raw_availability = doc.xpath(
            '//div[@id ="ProductBuy"]//button[contains(@class, "btn-primary")]//text()'
        )
        result = "".join(raw_availability).strip() if raw_availability else None

        if str(result).lower() in str("add to cart"):
            success(f"[{self.store_name}] {self.product_name} Available!")
            return True

        info(f"[{self.store_name}] {self.product_name} not available")
        return False
