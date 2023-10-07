import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


def post_new_order(access_token):
    post_order_endpoint_url = os.getenv("P2P_API_PATH") + 'orders'
    headers = {
        "Authorization": "Bearer " + access_token
    }
    order_req = requests.post(
        post_order_endpoint_url,
        headers=headers,
        json={
            "orderId": "98712372376427",
            "date": "2023-06-22T12:30:01",
            "card": "5555555555555555",
            "payoutAmount": 60000.00,
            "callbackUrl": os.getenv("OUR_CALLBACK_URL"),
            "callbackMethod": "PATCH",
            "callbackHeaders": json.dumps({
                "custom-header-key-1": "custom-header-value-1",
                "custom-header-key-2": "custom-header-value-2",
                "custom-header-key-3": "custom-header-value-3",
            }, separators=(',', ':')),
            "callbackBody": json.dumps({
                "custom-body-key-1": "custom-body-value-1",
                "custom-body-key-2": "custom-body-value-2"
            }, separators=(',', ':')),
        }
    )
    return order_req


def get_access_token() -> None or str:
    url = os.getenv("P2P_API_PATH") + "token/"
    token_req = requests.post(url, json={
        'username': os.getenv("TEST_USER_USERNAME"),
        'password': os.getenv("TEST_USER_PASSWORD")
    })
    print(token_req.text)
    if token_req.status_code == 200:
        token_res = token_req.json()
        token = token_res['access']
        print(token)
        return token

    return None


def create_new_order():
    access_token = get_access_token()
    if access_token is not None:
        order_req = post_new_order(access_token=access_token)
        print(order_req.content)
        return order_req.json()
