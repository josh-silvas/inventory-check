# -*- coding: utf-8 -*-
import requests

from util.log import success, info, fail
from typing import Dict


class Target:

    def __init__(self, product_info: Dict, cfg):
        self.cfg = cfg
        self.store_name = self.__class__.__name__
        self.product_id = product_info.get(self.store_name).get("_id")
        self.product_link = product_info.get(self.store_name).get("link")
        self.product_name = product_info.get("Name")

        s = requests.session()
        s.get("https://www.target.com")
        store_id = requests.get(
            "https://redsky.target.com/v3/stores/nearby/%s?key=%s&limit=1&within=100&unit=mile"
            % (s.cookies["GuestLocation"].split("|")[0], s.cookies["visitorId"])
        ).json()
        self.store_id = store_id[0]["locations"][0]["location_id"]

    def check_availability(self) -> bool:
        is_available = False
        for zip_code in self.cfg.target_zip_codes:
            try:
                amount, location = self.check_specific(zip_code)
                if amount > 0:
                    is_available = True
                    success(
                        f"[{self.store_name}] {self.product_name} {amount} units found {location}"
                    )
                else:
                    info(
                        f"[{self.store_name}] {self.product_name} not available in {zip_code}"
                    )
            except KeyError:
                fail(
                    f"[{self.store_name}] {self.product_name} could not find "
                    f"something in the list for {self.store_name}"
                )
        return is_available

    def check_specific(self, zip_code):
        req = requests.get(
            url=f"https://redsky.target.com/v1/location_details/{self.product_id}",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0",
                "Referer": "https://www.target.com",
                "Accept": "application/json",
            },
            params={"zip": zip_code, "state": "TX", "storeId": self.store_id},
        )
        data = req.json()
        status = str(
            data["product"]["available_to_promise_store"]["products"][0][
                "availability_status"
            ]
        )
        amount = int(
            data["product"]["available_to_promise_store"]["products"][0][
                "available_to_promise_quantity"
            ]
        )
        if status == str("OUT_OF_STOCK"):
            status = data["product"]["available_to_promise_network"][
                "availability_status"
            ]
            amount = int(
                data["product"]["available_to_promise_network"][
                    "available_to_promise_quantity"
                ]
            )
            if status == str("OUT_OF_STOCK"):
                return 0, "out of stock in network and stores"
            elif status == "IN_STOCK":
                return amount, "online"
            elif status == "PRE_ORDER_SELLABLE":
                return amount, "online"
        elif status == "IN_STOCK":
            return amount, "in store"
        elif status == "PRE_ORDER_SELLABLE":
            return amount, "in store"

        raise KeyError("Unknown status")
