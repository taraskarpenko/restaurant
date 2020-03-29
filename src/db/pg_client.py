import os
import logging
from typing import List, Any, Set, Tuple

import psycopg2
from psycopg2 import connect, extras
from werkzeug.datastructures import MultiDict

from src.models import Restaurant
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

connection = connect(**connection_params)
connection.autocommit = True


def insert_restaurant(data: Restaurant) -> None:
    with connection.cursor() as cursor:
        restaurant_query = qb.build_insert_restaurant_query(data)
        cursor.execute(restaurant_query)

        if data.tags:
            tags_query = qb.build_insert_tags_query(data.id, data.tags)
            cursor.execute(tags_query)


def get_restaurant_by_id(restaurant_id: str) -> Restaurant:
    with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
        get_restaurant_query = qb.build_get_restaurant_by_id_query(restaurant_id)
        cursor.execute(get_restaurant_query)
        restaurant = cursor.fetchone()
        if restaurant is None:
            raise psycopg2.DataError("Not found")

        get_tags_query = qb.build_get_tags_by_restaurant_id_query(restaurant_id)
        cursor.execute(get_tags_query)
        if cursor.rowcount > 0:
            tags = [row['tag'] for row in cursor.fetchall()]
        else:
            tags = None

        return Restaurant(tags=tags, **restaurant)


def delete_restaurant_by_id(restaurant_id: str) -> bool:
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
    with connection.cursor() as cursor:
        restaurant_query = qb.build_update_restaurant_query(restaurant)
        cursor.execute(restaurant_query)
        if cursor.rowcount == 0:
            raise psycopg2.DataError("Not found")
        elif cursor.rowcount > 1:
            raise psycopg2.DataError(f"Found {cursor.rowcount} rows while 1 was expected")

        tags_delete_query = qb.build_delete_tags_query(restaurant.id)
        cursor.execute(tags_delete_query)
        if restaurant.tags:
            tags_query = qb.build_insert_tags_query(restaurant.id, restaurant.tags)
            cursor.execute(tags_query)


def _get_all_restaurant_ids(cursor: Any) -> Set[str]:
    restaurant_ids = qb.build_select_all_restaurant_ids()
    cursor.execute(restaurant_ids)
    result = cursor.fetchall()
    return {t[0] for t in result}


def _get_restaurants_by_ids(final_ids_list: Set[str], cursor: Any) -> List[Restaurant]:
    restaurants_list_query = qb.build_select_restaurants_by_ids(final_ids_list)
    cursor.execute(restaurants_list_query)
    result = cursor.fetchall()
    return [Restaurant(**r) for r in result]


def _get_restaurants_by_tags(tags: Tuple[str], cursor: Any) -> Set[str]:
    restaurant_ids_by_tags_query = qb.build_select_restaurant_ids_by_tags_query(tags)
    cursor.execute(restaurant_ids_by_tags_query)
    result = cursor.fetchall()
    return {t[0] for t in result}


def _get_restaurant_ids_by_field(keys: set, args: MultiDict, cursor: Any) -> Set[str]:
    filters = {}
    for key in keys:
        transformed_key = key.replace('filter[', '').replace(']', '')
        filters[transformed_key] = args.getlist(key)

    restaurant_ids_by_field_query = qb.build_select_restaurant_ids_by_field_query(filters)
    print(restaurant_ids_by_field_query.as_string(cursor))
    cursor.execute(restaurant_ids_by_field_query)
    result = cursor.fetchall()
    return {t[0] for t in result}


def select_restaurants_by_filters(args: MultiDict) -> List[Restaurant]:
    with connection.cursor() as cursor:

        if len(list(args.keys())) == 0:
            final_ids_list = _get_all_restaurant_ids(cursor)
        else:

            restaurant_filter_keys = set(filter(lambda k: k != 'filter[tag]', args.keys()))
            if len(restaurant_filter_keys) > 0:
                q_result = _get_restaurant_ids_by_field(restaurant_filter_keys, args, cursor)
            else:
                q_result = _get_all_restaurant_ids(cursor)
            if 'filter[tag]' in args.keys():
                restaurant_ids_by_tags = _get_restaurants_by_tags(args.getlist('filter[tag]'), cursor)
                final_ids_list = q_result.intersection(restaurant_ids_by_tags)
            else:
                final_ids_list = q_result

    with connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
        restaurants = _get_restaurants_by_ids(final_ids_list, cursor)

    return restaurants
