from typing import Tuple, Set, List

from psycopg2 import sql

from src.models import Restaurant


def build_insert_tags_query(restaurant_id: str, tags: List[str]) -> sql.Composed:
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


def build_insert_restaurant_query(data: Restaurant) -> sql.Composed:
    restaurant_query = sql.SQL("""
            INSERT INTO restaurant (id, name, 
                                    country, zip_code, city, address_line_1, 
                                    longitude, latitude, 
                                    service_type, cuisine, web_address)
            VALUES ({id}, {name},
                    {country}, {zip_code}, {city}, {address_line_1},
                    {longitude}, {latitude},
                    {service_type}, {cuisine}, {web_address})
            """).format(
        id=sql.Literal(data.id),
        name=sql.Literal(data.name),
        country=sql.Literal(data.country),
        zip_code=sql.Literal(data.zip_code),
        city=sql.Literal(data.city),
        address_line_1=sql.Literal(data.address_line_1),
        longitude=sql.Literal(data.longitude),
        latitude=sql.Literal(data.latitude),
        service_type=sql.Literal(data.service_type),
        cuisine=sql.Literal(data.cuisine),
        web_address=sql.Literal(data.web_address),
    )
    return restaurant_query


def build_get_restaurant_by_id_query(restaurant_id: str) -> sql.Composed:
    get_restaurant_query = sql.SQL("""
                        SELECT id, name, 
                                country, zip_code, city, address_line_1, 
                                longitude, latitude, 
                                service_type, cuisine, web_address
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
            SET name={name}, 
                country={country}, zip_code={zip_code}, city={city}, address_line_1={address_line_1},
                longitude={longitude}, latitude={latitude},
                service_type={service_type}, cuisine={cuisine}, web_address={web_address}
            WHERE id={id}
            """).format(
        id=sql.Literal(data.id),
        name=sql.Literal(data.name),
        country=sql.Literal(data.country),
        zip_code=sql.Literal(data.zip_code),
        city=sql.Literal(data.city),
        address_line_1=sql.Literal(data.address_line_1),
        longitude=sql.Literal(data.longitude),
        latitude=sql.Literal(data.latitude),
        service_type=sql.Literal(data.service_type),
        cuisine=sql.Literal(data.cuisine),
        web_address=sql.Literal(data.web_address),
    )
    return restaurant_query


def build_delete_tags_query(restaurant_id: str) -> sql.Composed:
    delete_tags_query = sql.SQL("""
            DELETE FROM tags
            WHERE restaurant_id = {restaurant_id}
            """).format(
        restaurant_id=sql.Literal(restaurant_id),
    )
    return delete_tags_query


def build_select_all_restaurant_ids() -> sql.Composed:
    query = sql.SQL("""
                SELECT distinct id 
                FROM restaurant 
                """)
    return sql.Composed(query)


def build_select_restaurants_by_ids(ids: Set[str]) -> sql.Composed:
    get_restaurants_query = sql.SQL("""
                            SELECT id, name,
                                    country, zip_code, city, address_line_1, 
                                    longitude, latitude,
                                    service_type, cuisine, web_address
                            FROM restaurant
                            WHERE id IN ({ids})
                            """).format(
        ids=sql.SQL(',').join(map(sql.Literal, ids))
    )
    return get_restaurants_query


def build_select_restaurant_ids_by_tags_query(tags: Tuple[str]) -> sql.Composed:
    query = sql.SQL("""
                SELECT distinct restaurant_id
                FROM tags
                WHERE tag IN ({})
                """).format(
        sql.SQL(',').join(map(sql.Literal, tags))
    )
    return query


def build_select_restaurant_ids_by_field_query(filters: dict) -> sql.Composed:
    keys_templates = []
    values = []
    for k, v in filters.items():
        keys_templates.append(str(k) + " in ({})")
        values.append(v)
    where_clause_template = " AND ".join(keys_templates)

    query_header = "SELECT distinct id FROM restaurant WHERE "
    query = sql.SQL(query_header + where_clause_template).format(
        *[sql.SQL(',').join(map(sql.Literal, values_for_key)) for values_for_key in values]
    )
    return query
