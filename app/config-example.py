"""
config-example.py is an example of the config.py file that this script will read from for
user-specific information. Once you download this script, you will need to:
 1. Copy config-example.py to config.py.
 2. Populate config.py with your own information.
"""

# SMS will be used with the twilio client to send text messages to you. If you do
# not chose to use the SMS service, simply do not add any credentials here and it should
# skip it in process.
# If you would like to enable SMS message support, you can get a free Twilio account here
# - https://www.twilio.com/
SMS = {
    "from_number": 0,
    "to_number": 0,
    "account_sid": "",
    "auth_token": "",
}

# BEST_BUY_API_KEY is used with the Best Buy class. If you do not enter an API key here,
# then Best Buy will be skipped as a checkable store. If you chose to use Best Buy, you can
# sign up for an API key for free from the Best Buy developer portal:
#  - https://developer.bestbuy.com/login
BEST_BUY_API_KEY = ""

# TARGET_ZIP_CODES is a listing of zip codes for the Target class to check for pick-up availability.
# If do not enter any zip codes, pick-up checks will be skipped.
TARGET_ZIP_CODES = []

# POLL_INTERVAL is the time in seconds that this script will wait before running a check against the
# listed stores again. The default is every 10 minutes (600 seconds).
POLL_INTERVAL = 600
