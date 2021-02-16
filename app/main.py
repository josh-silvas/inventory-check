#!/usr/bin/python3
import time

from config import Config
from util import Twilio
from store import Amazon, BestBuy, NewEgg, Target, WalMart
from products import INFO

# ACTIVE_STORES is a list of the active store classes that this script will check.
# Each stores class name will coincide with a product.INFO key, so make sure those
# match.
ACTIVE_STORES = [BestBuy, Amazon, Target, WalMart, NewEgg]


def main():
    while True:
        config = Config()

        # Initialize a Twilio client. If you choose to not use one, then do not populate
        # twilio information (SMS) in the config.py file.
        message = Twilio(config)

        # Range through the list of active products listed in the products dictionary.
        for product_info in INFO:

            # Check all the ACTIVE_STORES from the constant above.
            for store in ACTIVE_STORES:

                # This is a check to see if the implemented store class name exist as a key in the
                # product infos, if it does not, then we will skip this store for this product.
                if not product_info.get(store.__name__):
                    print(
                        f"{store.__name__} does not have a configuration item. "
                        f"Please check config.py for an entry. Skipping..."
                    )
                    continue

                # Finally we run the check_availability method on the Store class implementation. This
                # method should handle any print statements to screen and only return a boolean indicating
                # if the store has the product available.
                if store(product_info, config).check_availability():
                    message.send(
                        f"{store.__name__} has {product_info['Name']} in stock!!!"
                    )

        # Sit and wait for the poll interval duration before processing this loop again.
        time.sleep(config.poll_interval)


if __name__ == "__main__":
    main()
