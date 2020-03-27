import logging

from flask import Request

from . import models
from .db import pg_client as db
from .serialization import RestaurantRequestSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handle_post_restaurant(request: Request) -> models.Restaurant:
    create_restaurant_request = RestaurantRequestSchema().load(request.json)
    db.insert_restaurant(create_restaurant_request)
    return create_restaurant_request


def handle_get_restaurant_by_id(restaurant_id: str) -> models.Restaurant:
    return db.get_restaurant_by_id(restaurant_id)


def handle_delete_restaurant_by_id(restaurant_id: str) -> bool:
    return db.delete_restaurant_by_id(restaurant_id)


def handle_update_restaurant_by_id(restaurant_id: str, request: Request) -> models.Restaurant:
    update_restaurant_request = RestaurantRequestSchema().load(request.json)
    update_restaurant_request.id = restaurant_id
    db.update_restaurant(update_restaurant_request)
    return update_restaurant_request
