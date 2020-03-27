import logging
import os

from flask import Flask, request, jsonify
from marshmallow import ValidationError
from psycopg2._psycopg import DataError

from src import views

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

FLASK_RUN_PORT = int(os.getenv('FLASK_RUN_PORT', '5000'))
FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST', '127.0.0.1')


@app.route('/ping', methods=['GET'])
def ping():
    return 'success', 200


@app.route('/restaurant', methods=['POST'])
def restaurant():
    try:
        result = views.handle_post_restaurant(request)
        return jsonify(result), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as ex:
        return str(ex), 500


@app.route('/restaurant/<uuid>', methods=['GET', 'PUT', 'DELETE'])
def restaurant_by_id(uuid):
    try:
        if request.method == 'GET':
            result = views.handle_get_restaurant_by_id(uuid)
            return jsonify(result), 200
        elif request.method == 'PUT':
            result = views.handle_update_restaurant_by_id(uuid, request)
            return jsonify(result), 200
        elif request.method == 'DELETE':
            views.handle_delete_restaurant_by_id(uuid)
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
