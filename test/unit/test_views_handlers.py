from unittest.mock import patch

import pytest
from werkzeug.datastructures import MultiDict

from src import app
from src.app import handle_get_restaurant_by_id, handle_delete_restaurant_by_id, handle_update_restaurant_by_id, \
    list_restaurants_by_filters


@patch('src.db.pg_client.select_restaurants_by_filters')
def test_list_restaurants_by_filters_fails_for_unsupported_key(db_patch):
    data = MultiDict()
    data.add('not_a_filter', 'not_a_value')
    with pytest.raises(ValueError) as value_error:
        def f():
            list_restaurants_by_filters(data)

        f()
    expected_error_message = "Unsupported filter: not_a_filter"
    assert value_error.value.args[0] == expected_error_message


@patch('src.db.pg_client.select_restaurants_by_filters')
def test_list_restaurants_by_filters(db_patch):
    data = MultiDict()
    data.add('filter[tag]', 'tag_1')
    data.add('filter[tag]', 'tag_1')

    list_restaurants_by_filters(data)
    db_patch.assert_called_once_with(data)


@patch('src.db.pg_client.insert_restaurant')
@patch('src.serialization.RestaurantRequestSchema.load')
def test_handle_post_restaurant(schema_load_patch, db_patch):
    schema_load_patch.return_value("123")

    app.handle_post_restaurant({"key": "value"})

    schema_load_patch.assert_called_once_with({"key": "value"})
    db_patch.call_args[0][0].assert_called_once_with("123")


@patch('src.db.pg_client.get_restaurant_by_id')
def test_handle_get_restaurant_by_id(db_patch):
    handle_get_restaurant_by_id("123")
    db_patch.assert_called_once_with("123")


@patch('src.db.pg_client.delete_restaurant_by_id')
def test_handle_delete_restaurant_by_id(db_patch):
    handle_delete_restaurant_by_id("123")
    db_patch.assert_called_once_with("123")


@patch('src.db.pg_client.update_restaurant')
@patch('src.serialization.RestaurantRequestSchema.load')
def test_handle_update_restaurant_by_id(schema_load_patch, db_patch):
    schema_load_patch.return_value("123")
    handle_update_restaurant_by_id("id-1", {"key": "value"})

    schema_load_patch.assert_called_once_with({"key": "value"})
    db_patch.call_args[0][0].assert_called_once_with("123")
