import logging
import os
from typing import List

from flask import Flask, request, jsonify, Request
from flask_caching import Cache
from marshmallow import ValidationError
from psycopg2._psycopg import DataError
from werkzeug.datastructures import MultiDict

import src.db.pg_client as db
from src import models
from src.serialization import RestaurantRequestSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = {
    "DEBUG": False,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 1200
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

FLASK_RUN_PORT = int(os.getenv('FLASK_RUN_PORT', '5000'))
FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST', '127.0.0.1')


def handle_post_restaurant(rq_json: dict) -> models.Restaurant:
    create_restaurant_request = RestaurantRequestSchema().load(rq_json)
    db.insert_restaurant(create_restaurant_request)

    cache.delete_memoized(list_restaurants_by_filters)
    return create_restaurant_request

@cache.memoize()
def handle_get_restaurant_by_id(restaurant_id: str) -> models.Restaurant:
    return db.get_restaurant_by_id(restaurant_id)


def handle_delete_restaurant_by_id(restaurant_id: str) -> bool:
    result = db.delete_restaurant_by_id(restaurant_id)
    cache.delete_memoized(handle_get_restaurant_by_id, restaurant_id)
    cache.delete_memoized(list_restaurants_by_filters)
    return result


def handle_update_restaurant_by_id(restaurant_id: str, request_json: dict) -> models.Restaurant:
    cache.delete_memoized(handle_get_restaurant_by_id, restaurant_id)
    cache.delete_memoized(list_restaurants_by_filters)

    update_restaurant_request = RestaurantRequestSchema().load(request_json)
    update_restaurant_request.id = restaurant_id
    db.update_restaurant(update_restaurant_request)
    return update_restaurant_request


@cache.memoize()
def list_restaurants_by_filters(args: MultiDict) -> List[models.Restaurant]:
    supported_filters = ['filter[tag]',
                         'filter[cuisine]',
                         'filter[service_type]',
                         'filter[city]']
    for key in args.keys():
        if key not in supported_filters:
            raise ValueError(f"Unsupported filter: {key}")

    result = db.select_restaurants_by_filters(args)
    return result


@app.route('/ping', methods=['GET'])
def ping():
    return 'success', 200


@app.route('/restaurant', methods=['GET', 'POST'])
def restaurant():
    if request.method == 'POST':
        try:
            result = handle_post_restaurant(request.json)
            return jsonify(result), 201
        except ValidationError as err:
            return jsonify(err.messages), 400
        except Exception as ex:
            return str(ex), 500
    elif request.method == 'GET':
        # TODO add pagination
        try:
            result = list_restaurants_by_filters(request.args)
            return jsonify(result), 200
        except ValueError as value_error:
            return str(value_error), 400
        except Exception as ex:
            return str(ex), 500


@app.route('/restaurant/<uuid>', methods=['GET', 'PUT', 'DELETE'])
def restaurant_by_id(uuid):
    try:
        if request.method == 'GET':
            result = handle_get_restaurant_by_id(uuid)
            return jsonify(result), 200
        elif request.method == 'PUT':
            result = handle_update_restaurant_by_id(uuid, request.json)
            return jsonify(result), 200
        elif request.method == 'DELETE':
            handle_delete_restaurant_by_id(uuid)
            return jsonify({'success': True}), 200
    except ValidationError as validation_error:
        return jsonify(validation_error.messages), 400
    except DataError as data_error:
        return str(data_error), 404
    except Exception as ex:
        return str(ex), 500


if __name__ == '__main__':
    logging.warning("Only for local run!")
    app.run(host=FLASK_RUN_HOST, port=FLASK_RUN_PORT)
