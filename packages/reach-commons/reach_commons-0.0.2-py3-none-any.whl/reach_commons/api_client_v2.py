import json

import requests
from requests.structures import CaseInsensitiveDict


class ReachApiGatewayV2:
    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.headers = CaseInsensitiveDict(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "authorization": f"Bearer {access_token}",
            }
        )

    def stripe_create_subscription(self, user_id, business_id, data):
        resp = requests.post(
            f"{self.base_url}/stripe/user/{user_id}/business/{business_id}/subscription",
            headers=self.headers,
            data=json.dumps(data)
        )
        return resp
