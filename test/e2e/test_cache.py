import uuid
from uuid import UUID

from psycopg2 import connect

import test.e2e.test_data.crud_test_data as t_data
from src.db.pg_client import connection_params
from test.e2e import e2e_test_base


class TestCache(e2e_test_base.E2ETestBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.connection = connect(**connection_params)
        cls.connection.autocommit = True

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.connection.close()

    def test_get_by_id_restaurant_cached(self):
        payload = t_data.restaurant_1_full_payload()
        restaurant_id = self.post_restaurant(payload)
        self.restaurants.append(restaurant_id)
        self.get_restaurant(restaurant_id, payload)
        self.get_restaurant(restaurant_id, payload)

        with self.connection.cursor() as cursor:
            query = """
                UPDATE restaurant
                SET service_type='shop', cuisine='alcohol'
                WHERE id='{}'
            """.format(restaurant_id)
            cursor.execute(query)

        self.get_restaurant(restaurant_id, payload)

        with self.connection.cursor() as cursor:
            query = """
                SELECT service_type, cuisine
                FROM restaurant
                WHERE id='{}'
            """.format(restaurant_id)
            cursor.execute(query)
            res = cursor.fetchone()
            self.assertEqual(res[0], "shop", "DB was not updated, possible false positive")
            self.assertEqual(res[1], "alcohol", "DB was not updated, possible false positive")

        self.get_restaurant(restaurant_id, payload)

    def test_get_full_list_cached(self):
        from test.e2e.sample_data import import_data, data
        bulk_restaurant_ids = import_data.import_restaurants(10)
        self.restaurants.extend(bulk_restaurant_ids)
        restaurants_list = self.get_restaurants_full_list()
        list_length = len(restaurants_list)

        fake_restaurant_id = str(uuid.uuid4())
        self.restaurants.append(fake_restaurant_id)
        with self.connection.cursor() as cursor:
            query = """
                INSERT INTO restaurant 
                (id, name, country, zip_code, city, address_line_1, longitude, latitude)
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
            """.format(fake_restaurant_id, "", "", "", "", "", "", "")
            cursor.execute(query)

        new_restaurants_list = self.get_restaurants_full_list()
        new_list_length = len(new_restaurants_list)
        self.assertEqual(new_list_length, list_length)

    def test_get_list_by_filters_cached(self):
        pass
