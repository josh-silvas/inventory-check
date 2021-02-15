import requests
from typing import List
from time import sleep
from util.log import success, info, fail
from config import BEST_BUY_API_KEY


class BestBuy:
    def __init__(self, product_info):
        self.store_name = self.__class__.__name__
        self.product_id = product_info.get(self.store_name).get("_id")
        self.product_link = product_info.get(self.store_name).get("link")
        self.product_name = product_info.get("Name")

    def check_availability(self) -> bool:
        sleep(1)
        is_available = False
        if self._print(self._available_within_zip(int(self.product_id))):
            is_available = True
        sleep(1)
        if self._print(self._available_online(int(self.product_id))):
            is_available = True
        return is_available

    def _print(self, result) -> bool:
        if len(result) == 0:
            info(f"[{self.store_name}] {self.product_name} not available.")
            return False

        for elem in result:
            success(f"[{self.store_name}] {self.product_name} Available {elem}!")
            return True

    def _available_within_zip(self, sku: int, zip_code: int = 78261) -> List[str]:
        r = requests.get(
            url=f"{self.product_link}/products/{sku}/stores.json",
            params={"apiKey": BEST_BUY_API_KEY, "postalCode": zip_code},
        )
        ret_val = []
        if r.status_code > 209:
            content = r.content.replace(b"\n", b"").replace(b"\r", b"").replace(b"  ", b"")
            fail(f"ConnectionError: Received {r.status_code}: {content}")
            return ret_val
        resp = r.json()
        if not resp.get("stores"):
            return ret_val
        for elem in resp.get("stores"):
            ret_val.append(elem["name"])
        return ret_val

    def _available_online(self, sku: int) -> List[str]:
        r = requests.get(
            url=f"{self.product_link}/products(sku={sku})",
            params={
                "apiKey": BEST_BUY_API_KEY,
                "show": ",".join(["onlineAvailability", "sku", "name", "addToCartUrl"]),
                "format": "json",
                "sort": "onlineAvailability.asc",
            },
        )
        ret_val = []
        if r.status_code > 209:
            content = r.content.replace(b"\n", b"").replace(b"\r", b"").replace(b"  ", b"")
            fail(f"ConnectionError: Received {r.status_code}: {content}")
            return ret_val
        resp = r.json()
        if not resp.get("products"):
            return ret_val
        for elem in resp.get("products"):
            if elem["onlineAvailability"]:
                return ["Online"]
        return ret_val
