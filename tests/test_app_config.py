import unittest

from app.config import Config


class TestConfig(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestConfig, self).__init__(*args, **kwargs)
        self.config = Config("app/config-example.ini")

    def test_attributes(self):
        self.assertEqual(self.config.poll_interval, 30)
        self.assertEqual(self.config.target_zip_codes, ['60661'])
        self.assertIsNone(self.config.best_buy_api_key)
        self.assertIsNone(self.config.sms_auth_token)
        self.assertIsNone(self.config.sms_account_sid)
        self.assertIsNone(self.config.sms_to_number)
        self.assertIsNone(self.config.sms_from_number)
