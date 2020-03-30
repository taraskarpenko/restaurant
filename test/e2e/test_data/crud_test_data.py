def restaurant_1_full_payload():
    payload = {
        'name': 'Pomodori',
        'country': 'Germany',
        'city': 'Potsdam',
        'zip_code': '14473',
        'address_line_1': 'Babelsberger Str. 1',
        'cuisine': 'Italian',
        'longitude': '13.067141',
        'latitude': '52.391592',
        'service_type': 'serviced',
        'web_address': 'www.example.com',
        'tags': ["italian", "pizza", "pasta"]
    }
    return payload


def restaurant_1_only_required_payload():
    payload = {
        'name': 'Pomodori',
        'country': 'Germany',
        'city': 'Potsdam',
        'zip_code': '14473',
        'address_line_1': 'Babelsberger Str. 1',
        'longitude': '13.067141',
        'latitude': '52.391592',
    }
    return payload


def restaurant_2_full_payload():
    payload = {
        'name': 'Peter Pane',
        'country': 'Germany',
        'city': 'Berlin',
        'zip_code': '10117',
        'address_line_1': 'Friedrichstraße 101',
        'cuisine': 'American',
        'longitude': '13.999999',
        'latitude': '52.999999',
        'service_type': 'self_service',
        'web_address': 'www.example.com',
        'tags': ["burger", "bbq"]
    }
    return payload


def restaurant_with_incorrect_types():
    payload = {
        'name': 1,
        'country': 2,
        'city': 3,
        'zip_code': 4,
        'address_line_1': 5,
        'cuisine': 6,
        'longitude': 13.999999,
        'latitude': 52.999999,
        'service_type': ['self_service'],
        'web_address': ['www.example.com'],
        'tags': "burger"
    }
    return payload


def error_response_for_incorrect_types():
    response = {
        'address_line_1': ['Not a valid string.'],
        'city': ['Not a valid string.'],
        'country': ['Not a valid string.'],
        'cuisine': ['Not a valid string.'],
        'latitude': ['Not a valid string.'],
        'longitude': ['Not a valid string.'],
        'name': ['Not a valid string.'],
        'service_type': ['Not a valid string.'],
        'tags': ['Not a valid list.'],
        'web_address': ['Not a valid string.'],
        'zip_code': ['Not a valid string.']
    }
    return response
