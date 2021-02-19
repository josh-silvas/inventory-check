import requests
from typing import List, Dict
from time import sleep
from app.util.log import success, info, fail


class BestBuy:
    def __init__(self, product_info: Dict, cfg):
        self.cfg = cfg
        self.store_name = self.__class__.__name__
        self.product_id = product_info.get(self.store_name).get("_id")
        self.product_link = product_info.get(self.store_name).get("link")
        self.product_name = product_info.get("Name")

    def check_availability(self) -> bool:
        if not self.cfg.best_buy_api_key:
            info(f"[{self.store_name}] api key missing. Skipping...")
            return False

        sleep(1)
        is_available = False
        if self._print(self.available_within_zip(int(self.product_id))):
            is_available = True
        sleep(1)
        if self._print(self.available_online(int(self.product_id))):
            is_available = True
        return is_available

    def _print(self, result) -> bool:
        if len(result) == 0:
            info(f"[{self.store_name}] {self.product_name} not available.")
            return False

        for elem in result:
            success(f"[{self.store_name}] {self.product_name} Available {elem}!")
            return True

    def available_within_zip(self, sku: int, zip_code: int = 78261) -> List[str]:
        r = requests.get(
            url=f"{self.product_link}/products/{sku}/stores.json",
            params={"apiKey": self.cfg.best_buy_api_key, "postalCode": zip_code},
        )

        if r.status_code > 209:
            content = (
                r.content.replace(b"\n", b"").replace(b"\r", b"").replace(b"  ", b"")
            )
            fail(f"ConnectionError: Received {r.status_code}: {content}")
            return []
        print(r.json())
        return self.check_within_zip_inventory(r.json())

    @staticmethod
    def check_within_zip_inventory(data):
        ret_val = []
        if not data.get("stores"):
            return ret_val
        for elem in data.get("stores"):
            ret_val.append(elem["name"])
        return ret_val

    def available_online(self, sku: int) -> List[str]:
        r = requests.get(
            url=f"{self.product_link}/products(sku={sku})",
            params={
                "apiKey": self.cfg.best_buy_api_key,
                "show": ",".join(["onlineAvailability", "sku", "name", "addToCartUrl"]),
                "format": "json",
                "sort": "onlineAvailability.asc",
            },
        )
        if r.status_code > 209:
            content = (
                r.content.replace(b"\n", b"").replace(b"\r", b"").replace(b"  ", b"")
            )
            fail(f"ConnectionError: Received {r.status_code}: {content}")
            return []
        print(r.json())
        return self.check_online_inventory(r.json())

    @staticmethod
    def check_online_inventory(data):
        ret_val = []
        if not data.get("products"):
            return ret_val
        for elem in data.get("products"):
            if elem["onlineAvailability"]:
                return ["Online"]
        return ret_val
