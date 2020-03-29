def full_valid_restaurant_request_payload():
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


def valid_restaurant_request_without_optionals_payload():
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


def full_invalid_restaurant_request_payload():
    payload = {
            'name': 123,
            'country': ['Germany'],
            'city': 'Potsdam',
            'zip_code': 14473,
            'address_line_1': ['Babelsberger Str. 1'],
            'cuisine': ['Italian'],
            'longitude': 13.067141,
            'latitude': 52.391592,
            'service_type': 'serviced',
            'web_address': 'www.example.com',
            'tags': [123]
    }
    return payload
