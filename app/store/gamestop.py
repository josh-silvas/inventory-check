from lxml import html
from app.util.log import success, info
import requests


class GameStop:
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
                "Referer": "https://www.gamestop.com/",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "authority": "9300303.fls.doubleclick.net",
                "scheme": "https",
                "sec-fetch-dest": "iframe",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "cross-site",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36",
            },
        )
        if page.status_code > 300:
            return False
        doc = html.fromstring(page.content)
        raw_availability = doc.xpath(
            '//div[contains(@class, "primary-details-row")]//'
            'button[contains(@class, "add-to-cart")]//text()'
        )

        result = "".join(raw_availability).strip() if raw_availability else None
        if str(result).lower() in str("Not Available").lower():
            info(f"[{self.store_name}] {self.product_name} not available.")
            return False

        if str(result).lower() in str("Add to cart").lower():
            success(f"[{self.store_name}] {self.product_name} Available!")
            return True

        info(f"[{self.store_name}] {self.product_name} not available.")
        return False
