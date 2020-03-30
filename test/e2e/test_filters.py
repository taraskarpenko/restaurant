import requests
from parameterized import parameterized

import test.e2e.test_data.filters_test_data as t_data
from test.e2e.e2e_test_base import E2ETestBase


class TestFilters(E2ETestBase):

    @classmethod
    def post_restaurant(cls, payload):
        post_response = requests.post(cls.RESTAURANT_URL, json=payload)
        post_response.raise_for_status()
        restaurant_id = post_response.json()['id']
        return restaurant_id

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print(f"Will inject restaurants")
        for restaurant in t_data.restaurants_list():
            restaurant_id = cls.post_restaurant(restaurant)
            cls.restaurants.append(restaurant_id)

    @parameterized.expand(
        [
            (
                    "filter[tag]=abc",
                    4
            ),
            (
                    "filter[tag]=abc&filter[tag]=cdf",
                    5
            ),
            (
                    "filter[tag]=abc&filter[cuisine]=Mexican&filter[tag]=cdf",
                    3
            ),
            (
                    "filter[cuisine]=Mexican&filter[tag]=cdf&filter[cuisine]=Italian",
                    5
            ),
            (
                    "filter[cuisine]=Mexican&filter[tag]=cdf&filter[cuisine]=Italian&filter[city]=Bonn",
                    2
            ),
            (
                    "filter[cuisine]=Mexican&filter[tag]=cdf&filter[cuisine]=Italian&filter[city]=Bonn"
                    "&filter[service_type]=serviced",
                    1
            )
        ]
    )
    def test_filters(self, filter_string, expected_qty):
        response = self.get_restaurants_by_filters(filter_string)
        self.assertEqual(expected_qty, len(response),
                         f"Unexpected quantity of restaurants returned by filter {filter_string}")
