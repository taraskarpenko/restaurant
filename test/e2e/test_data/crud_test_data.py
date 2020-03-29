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
