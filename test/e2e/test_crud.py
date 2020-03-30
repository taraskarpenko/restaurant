from parameterized import parameterized

import test.e2e.test_data.crud_test_data as t_data
from test.e2e.e2e_test_base import E2ETestBase


class TestCRUD(E2ETestBase):

    @parameterized.expand(
        [
            ("full payload", t_data.restaurant_1_full_payload()),
            ("minimal payload", t_data.restaurant_1_only_required_payload())
        ]
    )
    def test_post_get_restaurant(self, name, payload):
        restaurant_id = self.post_restaurant(payload)
        self.restaurants.append(restaurant_id)
        self.get_restaurant(restaurant_id, payload)

    def test_update_restaurant(self):
        initial_payload = t_data.restaurant_1_full_payload()
        update_1_payload = t_data.restaurant_1_only_required_payload()
        update_2_payload = t_data.restaurant_2_full_payload()

        restaurant_id = self.post_restaurant(initial_payload)
        self.restaurants.append(restaurant_id)
        self.get_restaurant(restaurant_id, initial_payload)

        self.update_restaurant(restaurant_id, update_1_payload)
        self.get_restaurant(restaurant_id, update_1_payload)

        self.update_restaurant(restaurant_id, initial_payload)
        self.get_restaurant(restaurant_id, initial_payload)

        self.update_restaurant(restaurant_id, update_2_payload)
        self.get_restaurant(restaurant_id, update_2_payload)

    def test_delete_restaurant(self):
        payload = t_data.restaurant_1_full_payload()
        restaurant_id = self.post_restaurant(payload)
        self.restaurants.append(restaurant_id)
        self.get_restaurant(restaurant_id, payload)

        self.delete_restaurant(restaurant_id)
        self.get_restaurant(restaurant_id, payload, 404)

        self.delete_restaurant(restaurant_id, 404)

    def test_creation_fails_on_wrong_data_type(self):
        payload_all_fields_incorrect = t_data.restaurant_with_incorrect_types()
        expected_error_response = t_data.error_response_for_incorrect_types()
        error_response = self.post_restaurant_expected_fail(payload_all_fields_incorrect)

        self.assertEqual(error_response.json(), expected_error_response)
        self.assertEqual(error_response.status_code, 400)

    def test_creation_fails_on_missing_required_fields(self):
        payload = t_data.restaurant_1_full_payload()
        del payload['name']

        error_response = self.post_restaurant_expected_fail(payload)
        self.assertEqual(error_response.json(), {'name': ['Missing data for required field.']})
        self.assertEqual(error_response.status_code, 400)

    def test_update_fails_on_wrong_data_type(self):
        payload = t_data.restaurant_1_full_payload()
        restaurant_id = self.post_restaurant(payload)
        self.restaurants.append(restaurant_id)

        payload['tags'] = "burger"
        error_response = self.post_restaurant_expected_fail(payload)

        self.assertEqual(error_response.json(), {'tags': ['Not a valid list.']})
        self.assertEqual(error_response.status_code, 400)

    def test_update_fails_on_missing_required_fields(self):
        payload = t_data.restaurant_1_full_payload()
        restaurant_id = self.post_restaurant(payload)
        self.restaurants.append(restaurant_id)

        del payload['name']

        error_response = self.post_restaurant_expected_fail(payload)
        self.assertEqual(error_response.json(), {'name': ['Missing data for required field.']})
        self.assertEqual(error_response.status_code, 400)
