from typing import Tuple

from psycopg2 import sql

from src.models import Location, Address, Restaurant


def build_insert_tags_query(restaurant_id: str, tags: Tuple[str]) -> sql.Composed:
    tags_placeholders = ", ".join(
        [
            "({0}, {" + str(i + 1) + "})"
            for i in range(len(tags))
        ]
    )

    values = [sql.Literal(restaurant_id)]
    values.extend(map(sql.Literal, tags))
    tags_query = sql.SQL(
        "INSERT INTO tags (restaurant_id, tag) values " + tags_placeholders
    ).format(*values)
    return tags_query


def build_insert_location_query(restaurant_id: str, location: Location) -> sql.Composed:
    location_query = sql.SQL("""
            INSERT INTO location (restaurant_id, longitude, latitude)
            VALUES ({restaurant_id}, {longitude}, {latitude})
            """).format(
        restaurant_id=sql.Literal(restaurant_id),
        longitude=sql.Literal(location.longitude),
        latitude=sql.Literal(location.latitude)
    )
    return location_query


def build_insert_address_query(restaurant_id: str, address: Address) -> sql.Composed:
    address_query = sql.SQL("""
            INSERT INTO address (restaurant_id, country, zip_code, city, address_line_1)
            VALUES ({restaurant_id}, {country}, {zip_code}, {city}, {address_line_1})
            """).format(
        restaurant_id=sql.Literal(restaurant_id),
        country=sql.Literal(address.country),
        zip_code=sql.Literal(address.zip_code),
        city=sql.Literal(address.city),
        address_line_1=sql.Literal(address.address_line_1)
    )
    return address_query


def build_insert_restaurant_query(data: Restaurant) -> sql.Composed:
    restaurant_query = sql.SQL("""
            INSERT INTO restaurant
            VALUES ({id}, {name}, {service_type}, {cuisine}, {web_address})
            """).format(
        id=sql.Literal(data.id),
        name=sql.Literal(data.name),
        service_type=sql.Literal(data.service_type),
        cuisine=sql.Literal(data.cuisine),
        web_address=sql.Literal(data.web_address),
    )
    return restaurant_query


def build_get_restaurant_by_id_query(restaurant_id: str) -> sql.Composed:
    get_restaurant_query = sql.SQL("""
                        SELECT id, name, service_type, cuisine, web_address
                        FROM restaurant
                        WHERE id = {id}
                        """).format(
        id=sql.Literal(restaurant_id),
    )
    return get_restaurant_query


def build_get_tags_by_restaurant_id_query(restaurant_id: str) -> sql.Composed:
    get_tags_query = sql.SQL("""
            SELECT tag
            FROM tags
            WHERE restaurant_id = {restaurant_id}
            """).format(
        restaurant_id=sql.Literal(restaurant_id),
    )
    return get_tags_query


def build_get_address_by_restaurant_id_query(restaurant_id: str) -> sql.Composed:
    get_address_query = sql.SQL("""
            SELECT country, zip_code, city, address_line_1
            FROM address
            WHERE restaurant_id = {restaurant_id}
            """).format(
        restaurant_id=sql.Literal(restaurant_id),
    )
    return get_address_query


def build_get_location_by_restaurant_id_query(restaurant_id: str) -> sql.Composed:
    get_location_query = sql.SQL("""
            SELECT longitude, latitude
            FROM location
            WHERE restaurant_id = {restaurant_id}
            """).format(
        restaurant_id=sql.Literal(restaurant_id),
    )
    return get_location_query


def build_delete_restaurant_by_id_query(restaurant_id: str) -> sql.Composed:
    delete_restaurant_query = sql.SQL("""
            DELETE FROM restaurant
            WHERE id = {id}
            """).format(
        id=sql.Literal(restaurant_id),
    )
    return delete_restaurant_query


def build_update_restaurant_query(data: Restaurant) -> sql.Composed:
    restaurant_query = sql.SQL("""
            UPDATE restaurant
            SET name={name}, service_type={service_type}, cuisine={cuisine}, web_address={web_address}
            WHERE id={id}
            """).format(
        id=sql.Literal(data.id),
        name=sql.Literal(data.name),
        service_type=sql.Literal(data.service_type),
        cuisine=sql.Literal(data.cuisine),
        web_address=sql.Literal(data.web_address),
    )
    return restaurant_query


def build_update_location_query(restaurant_id: str, location: Location) -> sql.Composed:
    if location is None:
        location_query = sql.SQL("""
                    DELETE FROM location
                    WHERE restaurant_id = {restaurant_id}
                    """).format(
            restaurant_id=sql.Literal(restaurant_id),
        )
    else:
        location_query = sql.SQL("""
                INSERT INTO location (restaurant_id, longitude, latitude)
                VALUES ({restaurant_id}, {longitude}, {latitude})
                ON CONFLICT ON CONSTRAINT location_restaurant_id_key 
                DO UPDATE SET longitude={longitude}, latitude={latitude}
                """).format(
            restaurant_id=sql.Literal(restaurant_id),
            longitude=sql.Literal(location.longitude),
            latitude=sql.Literal(location.latitude)
        )
    return location_query


def build_update_address_query(restaurant_id: str, address: Address) -> sql.Composed:
    if address is None:
        address_query = sql.SQL("""
                DELETE FROM address
                WHERE restaurant_id = {restaurant_id}
                """).format(
            restaurant_id=sql.Literal(restaurant_id),
        )
    else:
        address_query = sql.SQL("""
                INSERT INTO address (restaurant_id, country, zip_code, city, address_line_1)
                VALUES ({restaurant_id}, {country}, {zip_code}, {city}, {address_line_1})
                ON CONFLICT ON CONSTRAINT address_restaurant_id_key 
                DO UPDATE SET country={country}, zip_code={zip_code}, city={city}, address_line_1={address_line_1}
                """).format(
            restaurant_id=sql.Literal(restaurant_id),
            country=sql.Literal(address.country),
            zip_code=sql.Literal(address.zip_code),
            city=sql.Literal(address.city),
            address_line_1=sql.Literal(address.address_line_1)
        )
    return address_query


def build_delete_tags_query(restaurant_id: str) -> sql.Composed:
    delete_tags_query = sql.SQL("""
                    DELETE FROM tags
                    WHERE restaurant_id = {restaurant_id}
                    """).format(
        restaurant_id=sql.Literal(restaurant_id),
    )
    return delete_tags_query
