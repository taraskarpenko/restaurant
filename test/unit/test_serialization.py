import pytest
from marshmallow import ValidationError

from src import models
from src.serialization import RestaurantRequestSchema
from test.unit import test_data


def test_serialize_full_payload_excluding_unexpected():
    payload = test_data.full_valid_restaurant_request_payload()
    payload['extra_field'] = 999
    actual_result = RestaurantRequestSchema().load(payload)

    del payload['extra_field']
    expected_result = models.Restaurant(actual_result.id, **payload)
    assert actual_result == expected_result


def test_serialize_only_required_fields():
    payload = test_data.valid_restaurant_request_without_optionals_payload()
    actual_result = RestaurantRequestSchema().load(payload)
    expected_result = models.Restaurant(actual_result.id, **payload)
    assert actual_result == expected_result


def test_serialize_fails_on_incorrect_type():
    payload = test_data.full_invalid_restaurant_request_payload()
    with pytest.raises(ValidationError) as validation_error:
        def f():
            RestaurantRequestSchema().load(payload)

        f()
    expected_error_message = {'longitude': ['Not a valid string.'], 'tags': {0: ['Not a valid string.']},
                              'address_line_1': ['Not a valid string.'], 'name': ['Not a valid string.'],
                              'country': ['Not a valid string.'], 'latitude': ['Not a valid string.'],
                              'cuisine': ['Not a valid string.'], 'zip_code': ['Not a valid string.']}
    assert validation_error.value.args[0] == expected_error_message


def test_serialize_fails_on_missing_required():
    payload = test_data.full_valid_restaurant_request_payload()
    del payload['name']
    del payload['city']
    with pytest.raises(ValidationError) as validation_error:
        def f():
            RestaurantRequestSchema().load(payload)

        f()
    expected_error_message = {'city': ['Missing data for required field.'],
                              'name': ['Missing data for required field.']}
    assert validation_error.value.args[0] == expected_error_message
