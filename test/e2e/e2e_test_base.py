import unittest

import requests


def dict_without_none_values(original_dict: dict):
    return {k: v for (k, v) in original_dict.items() if v is not None}


class E2ETestBase(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"
    RESTAURANT_URL = BASE_URL + "/restaurant"
    RESTAURANT_ID_URL = RESTAURANT_URL + "/{}"
    restaurants = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        res = requests.get(cls.BASE_URL + "/ping", timeout=10)
        if res.status_code != 200:
            raise ConnectionError("Server under test is not responding")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        while cls.restaurants:
            order_id = cls.restaurants.pop()
            res = requests.delete(cls.RESTAURANT_ID_URL.format(order_id), timeout=10)
            print(f'tear down: delete order {order_id} status {res.status_code}')

    def post_restaurant(self, payload):
        post_response = requests.post(self.RESTAURANT_URL, json=payload)
        post_response.raise_for_status()
        restaurant_id = post_response.json()['id']

        expected_post_response = payload.copy()
        expected_post_response['id'] = restaurant_id
        self.assertEqual(dict_without_none_values(post_response.json()), expected_post_response,
                         "POST returned unexpected data")

        return restaurant_id

    def post_restaurant_expected_fail(self, payload):
        post_response = requests.post(self.RESTAURANT_URL, json=payload)
        if post_response == 201:
            self.restaurants.append(post_response.json()['id'])
            raise AssertionError("Unexpected restaurant created")

        return post_response

    def get_restaurant(self, restaurant_id, expected_payload, expected_status_code=200):
        get_response = requests.get(self.RESTAURANT_ID_URL.format(restaurant_id))
        self.assertEqual(get_response.status_code, expected_status_code, "Unexpected status code")
        if expected_status_code == 200:
            expected_get_response = expected_payload.copy()
            expected_get_response['id'] = restaurant_id
            self.assertEqual(dict_without_none_values(get_response.json()), expected_get_response,
                             "Order stored with wrong data")

    def get_restaurants_full_list(self):
        list_response = requests.get(self.RESTAURANT_URL)
        list_response.raise_for_status()
        return list_response.json()

    def get_restaurants_by_filters(self, filters_string):
        list_response = requests.get(self.RESTAURANT_URL + "?" + filters_string)
        list_response.raise_for_status()
        return list_response.json()

    def update_restaurant(self, restaurant_id, payload):
        expected_payload = payload.copy()
        expected_payload['id'] = restaurant_id
        put_response = requests.put(self.RESTAURANT_ID_URL.format(restaurant_id), json=payload)
        self.assertEqual(dict_without_none_values(put_response.json()),
                         dict_without_none_values(expected_payload),
                         "Order stored with wrong data")

    def delete_restaurant(self, restaurant_id, expected_status_code=200):
        delete_response = requests.delete(self.RESTAURANT_ID_URL.format(restaurant_id))
        self.assertEqual(delete_response.status_code, expected_status_code, "Unexpected status code")
