from twilio.rest import Client
from config import SMS


class Twilio:
    def __init__(self):
        if not SMS["auth_token"] or not SMS["account_sid"]:
            self.client = None
        else:
            self.client = Client(SMS["account_sid"], SMS["auth_token"])

    def send(self, message: str):
        if not self.client:
            return
        self.client.messages.create(
            to=f"+{SMS['to_number']}", from_=f"+{SMS['from_number']}", body=message
        )
