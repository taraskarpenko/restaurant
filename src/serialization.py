import uuid

from marshmallow import Schema, fields, post_load

from src import models as m


class AddressSchema(Schema):
    country = fields.String(required=True)
    zip_code = fields.String(required=True)
    city = fields.String(required=True)
    address_line_1 = fields.String(required=True)

    @post_load
    def to_object(self, data):
        return m.Address(**data)


class LocationSchema(Schema):
    latitude = fields.String(required=True)
    longitude = fields.String(required=True)

    @post_load
    def to_object(self, data):
        return m.Location(**data)


class RestaurantRequestSchema(Schema):
    name = fields.String(required=True)
    address = fields.Nested(AddressSchema)
    location = fields.Nested(LocationSchema)
    service_type = fields.String()
    cuisine = fields.String()
    web_address = fields.String()
    tags = fields.List(fields.String())

    @post_load
    def to_object(self, data) -> m.Restaurant:
        restaurant_id = str(uuid.uuid4())
        return m.Restaurant(id=restaurant_id, **data)
