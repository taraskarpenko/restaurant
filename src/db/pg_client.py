import logging

import psycopg2
from psycopg2 import connect, extras

from src.models import Restaurant, Location, Address
from . import query_builders as qb

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# This data should not be here, it should come from deployment
DB_HOST = 'restaurant.csphlet8ffjy.us-east-2.rds.amazonaws.com'
DB_USER = 'restaurant_app'
DB_PASSWORD = 'SDflksdjflsk3sdf'
connection_params = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": "restaurant"
}


def insert_restaurant(data: Restaurant) -> None:
    with connect(**connection_params) as connection:
        with connection.cursor() as cursor:
            restaurant_query = qb.build_insert_restaurant_query(data)
            cursor.execute(restaurant_query)

            if data.location:
                location_query = qb.build_insert_location_query(data.id, data.location)
                cursor.execute(location_query)

            if data.address:
                address_query = qb.build_insert_address_query(data.id, data.address)
                cursor.execute(address_query)

            if data.tags:
                tags_query = qb.build_insert_tags_query(data.id, data.tags)
                cursor.execute(tags_query)


def get_restaurant_by_id(restaurant_id: str) -> Restaurant:
    with connect(**connection_params) as connection:
        with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            get_restaurant_query = qb.build_get_restaurant_by_id_query(restaurant_id)
            cursor.execute(get_restaurant_query)
            restaurant = cursor.fetchone()
            if restaurant is None:
                raise psycopg2.DataError("Not found")

            get_tags_query = qb.build_get_tags_by_restaurant_id_query(restaurant_id)
            cursor.execute(get_tags_query)
            tags = [row['tag'] for row in cursor.fetchall()]
            restaurant['tags'] = tags

            get_address_query = qb.build_get_address_by_restaurant_id_query(restaurant_id)
            cursor.execute(get_address_query)
            address_data = cursor.fetchone()
            if address_data is not None:
                restaurant['address'] = Address(**address_data)

            get_location_query = qb.build_get_location_by_restaurant_id_query(restaurant_id)
            cursor.execute(get_location_query)
            location_data = cursor.fetchone()
            if location_data is not None:
                restaurant['location'] = Location(**location_data)

            return Restaurant(**restaurant)


def delete_restaurant_by_id(restaurant_id: str) -> bool:
    with connect(**connection_params) as connection:
        with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            delete_restaurant_query = qb.build_delete_restaurant_by_id_query(restaurant_id)
            cursor.execute(delete_restaurant_query)
            if cursor.rowcount == 1:
                return True
            elif cursor.rowcount == 0:
                raise psycopg2.DataError("Not found")
            else:
                raise psycopg2.DataError(f"Found {cursor.rowcount} rows while 1 was expected")


def update_restaurant(restaurant):
    with connect(**connection_params) as connection:
        with connection.cursor() as cursor:
            restaurant_query = qb.build_update_restaurant_query(restaurant)
            cursor.execute(restaurant_query)
            if cursor.rowcount == 0:
                raise psycopg2.DataError("Not found")
            elif cursor.rowcount > 1:
                raise psycopg2.DataError(f"Found {cursor.rowcount} rows while 1 was expected")

            location_query = qb.build_update_location_query(restaurant.id, restaurant.location)
            cursor.execute(location_query)
            if cursor.rowcount == 0:
                raise psycopg2.DataError("Not found")
            elif cursor.rowcount > 1:
                raise psycopg2.DataError(f"Found {cursor.rowcount} rows while 1 was expected")

            address_query = qb.build_update_address_query(restaurant.id, restaurant.address)
            cursor.execute(address_query)
            if cursor.rowcount == 0:
                raise psycopg2.DataError("Not found")
            elif cursor.rowcount > 1:
                raise psycopg2.DataError(f"Found {cursor.rowcount} rows while 1 was expected")

            tags_delete_query = qb.build_delete_tags_query(restaurant.id)
            tags_query = qb.build_insert_tags_query(restaurant.id, restaurant.tags)
            cursor.execute(tags_delete_query)
            cursor.execute(tags_query)
