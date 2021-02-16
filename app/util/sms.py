import time

from twilio.rest import Client
from util import info


class Twilio:
    def __init__(self, cfg):
        self.cfg = cfg
        self.has_notified = {}
        self.hold_down = 86400
        if not self.cfg.sms_auth_token or not self.cfg.sms_account_sid:
            self.client = None
        else:
            self.client = Client(self.cfg.sms_account_sid, self.cfg.sms_auth_token)

    def send(self, message: str):
        if not self.client:
            return

        if self._should_notify(message):
            self.client.messages.create(
                to=f"+{self.cfg.sms_to_number}", from_=f"+{self.cfg.sms_from_number}", body=message
            )

    def _should_notify(self, message: str):
        """
        _should_notify is a helper function that will prevent spamming your phone if
        items show up in stock. You should get only one text message per product, per store, then
        text notifications will snooze for 24 hours.
        """
        current_time = int(time.time())
        # If there is not a has_notified entry for this message:
        if not self.has_notified.get(message):
            self.has_notified[message] = current_time + self.hold_down
            return True

        # If there is an entry in has_notified, but the timestamp is smaller than
        # the current timestamp:
        if self.has_notified[message] > current_time:
            info(
                f"Next notify time of {self.has_notified[message]} is still less than current time {current_time}"
            )
            return False

        # Finally, there is an entry, but it is now invalid because the current time exceeds the
        # has_notified entry. Now we delete the entry and notify:
        del self.has_notified[message]
        return True
