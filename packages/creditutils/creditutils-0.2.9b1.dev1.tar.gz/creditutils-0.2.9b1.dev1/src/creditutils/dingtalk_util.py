import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json


class Manager:
    def __init__(self, webhook, secret):
        self.webhook = webhook
        self.secret = secret

    def get_webhook_with_signature(self):
        webhook = self.webhook
        secret = self.secret
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        result = f'{webhook}&timestamp={timestamp}&sign={sign}'
        return result

    def send_map_data(self, data):
        headers = {"Content-Type": "application/json"}
        webhook = self.get_webhook_with_signature()
        return requests.post(webhook, data=json.dumps(data), headers=headers)


def send_map_data(webhook, secret, data):
    manager = Manager(webhook, secret)
    return manager.send_map_data(data)
