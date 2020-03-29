import uuid

from marshmallow import Schema, fields, post_load, EXCLUDE

from src import models


class RestaurantRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    name = fields.String(required=True)
    country = fields.String(required=True)
    zip_code = fields.String(required=True)
    city = fields.String(required=True)
    address_line_1 = fields.String(required=True)
    latitude = fields.String(required=True)
    longitude = fields.String(required=True)
    service_type = fields.String()
    cuisine = fields.String()
    web_address = fields.String()
    tags = fields.List(fields.String())

    @post_load
    def to_object(self, data, **kwargs) -> models.Restaurant:
        restaurant_id = str(uuid.uuid4())
        return models.Restaurant(id=restaurant_id, **data)
