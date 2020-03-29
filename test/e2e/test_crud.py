import pytest
import requests
from parameterized import parameterized

import test.e2e.test_data.crud_test_data as t_data
from test.e2e.e2e_test_base import E2ETestBase, dict_without_none_values


class TestCRUD(E2ETestBase):

    def _post_restaurant(self, payload):
        post_response = requests.post(self.BASE_URL, json=payload)
        post_response.raise_for_status()
        restaurant_id = post_response.json()['id']

        expected_post_response = payload.copy()
        expected_post_response['id'] = restaurant_id
        self.assertEqual(dict_without_none_values(post_response.json()), expected_post_response,
                         "POST returned unexpected data")

        return restaurant_id

    def _post_restaurant_expected_fail(self, payload):
        post_response = requests.post(self.BASE_URL, json=payload)
        if post_response == 201:
            self.orders.append(post_response.json()['id'])
            raise AssertionError("Unexpected restaurant created")

        return post_response

    def _get_restaurant(self, restaurant_id, expected_payload, expected_status_code=200):
        get_response = requests.get(self.ID_URL.format(restaurant_id))
        self.assertEqual(get_response.status_code, expected_status_code, "Unexpected status code")
        if expected_status_code == 200:
            expected_get_response = expected_payload.copy()
            expected_get_response['id'] = restaurant_id
            self.assertEqual(dict_without_none_values(get_response.json()), expected_get_response,
                             "Order stored with wrong data")

    def _update_restaurant(self, restaurant_id, payload):
        expected_payload = payload.copy()
        expected_payload['id'] = restaurant_id
        put_response = requests.put(self.ID_URL.format(restaurant_id), json=payload)
        self.assertEqual(dict_without_none_values(put_response.json()),
                         dict_without_none_values(expected_payload),
                         "Order stored with wrong data")

    def _delete_restaurant(self, restaurant_id, expected_status_code=200):
        delete_response = requests.delete(self.ID_URL.format(restaurant_id))
        self.assertEqual(delete_response.status_code, expected_status_code, "Unexpected status code")

    @parameterized.expand(
        [
            ("full payload", t_data.restaurant_1_full_payload()),
            ("minimal payload", t_data.restaurant_1_only_required_payload())
        ]
    )
    def test_post_get_restaurant(self, name, payload):
        restaurant_id = self._post_restaurant(payload)
        self.orders.append(restaurant_id)
        self._get_restaurant(restaurant_id, payload)

    def test_update_restaurant(self):
        initial_payload = t_data.restaurant_1_full_payload()
        update_1_payload = t_data.restaurant_1_only_required_payload()
        update_2_payload = t_data.restaurant_2_full_payload()

        restaurant_id = self._post_restaurant(initial_payload)
        self.orders.append(restaurant_id)
        self._get_restaurant(restaurant_id, initial_payload)

        self._update_restaurant(restaurant_id, update_1_payload)
        self._get_restaurant(restaurant_id, update_1_payload)

        self._update_restaurant(restaurant_id, initial_payload)
        self._get_restaurant(restaurant_id, initial_payload)

        self._update_restaurant(restaurant_id, update_2_payload)
        self._get_restaurant(restaurant_id, update_2_payload)

    def test_delete_restaurant(self):
        payload = t_data.restaurant_1_full_payload()
        restaurant_id = self._post_restaurant(payload)
        self.orders.append(restaurant_id)
        self._get_restaurant(restaurant_id, payload)

        self._delete_restaurant(restaurant_id)
        self._get_restaurant(restaurant_id, payload, 404)

        self._delete_restaurant(restaurant_id, 404)

    def test_creation_fails_on_wrong_data_type(self):
        payload = t_data.restaurant_1_full_payload()
        payload['name'] = 1


    def test_creation_fails_on_missing_required_fields(self):
        pass
