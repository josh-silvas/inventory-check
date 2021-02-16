from os import path
from configparser import ConfigParser


class Config:

    def __new__(cls, filename: str = "config.ini"):
        if not path.isfile(filename):
            raise FileExistsError(f"Are you sure you copied your own config.ini file?\n"
                                  f"Try `cp app/config-example.ini app/config.ini`")

        cls._config = ConfigParser()
        cls._config.read(filename)

        cls.poll_interval = 600
        if cls._config.has_section("default"):
            if cls._config["default"].get("poll_interval"):
                cls.poll_interval = cls._config.getint("default", "poll_interval")

        cls.sms_from_number = None
        cls.sms_to_number = None
        cls.sms_account_sid = None
        cls.sms_auth_token = None
        if cls._config.has_section("sms"):
            if cls._config["sms"].get("from_number"):
                cls.sms_from_number = cls._config["sms"].getint("from_number")

            if cls._config["sms"].get("to_number"):
                cls.sms_to_number = cls._config["sms"].getint("to_number")

            if cls._config["sms"].get("account_sid"):
                cls.sms_account_sid = cls._config["sms"].get("account_sid")

            if cls._config["sms"].get("auth_token"):
                cls.sms_auth_token = cls._config["sms"].get("auth_token")

        cls.best_buy_api_key = None
        if cls._config.has_section("best_buy"):
            if cls._config["best_buy"].get("api_key"):
                cls.best_buy_api_key = cls._config["best_buy"].get("api_key")

        cls.target_zip_codes = []
        if cls._config.has_section("target"):
            if cls._config["target"].get("zip_codes"):
                cls.target_zip_codes = cls._config["target"].get("zip_codes").split(",")

        return super(Config, cls).__new__(cls)

