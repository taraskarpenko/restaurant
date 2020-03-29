import unittest

import requests


def dict_without_none_values(original_dict: dict):
    return {k: v for (k, v) in original_dict.items() if v is not None}


class E2ETestBase(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/restaurant"
    ID_URL = BASE_URL + "/{}"
    orders = []

    def setUp(self):
        super().setUp()

    def tearDown(self):
        while self.orders:
            order_id = self.orders.pop()
            res = requests.delete(self.ID_URL.format(order_id), timeout=10)
            print(f'tear down: delete order {order_id} status {res.status_code}')
