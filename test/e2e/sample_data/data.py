import string
import random

restaurant_template = {
    "web_address": "www.example.com",
}

name_prefixes = ["", "The ", "Your ", "Premium "]
name_values = ["Lonesome Dove", "Easy Eats", "Golden Palace", "Quick Bite", "Blind Pig", "Dainty Dog", "Spicy Heat"]
name_postfixes = ["", " Grill", " Cafe", " Diner", " Bistro", " Tavern"]

cuisine_values = ["Asian", "Oriental", "Mediterranean", "American", "Chinese"]

service_type_values = ["self-service", "serviced", "fast-food"]

alphabet = string.ascii_lowercase


def name_generator():
    return random.choice(name_prefixes) + random.choice(name_values) + random.choice(name_postfixes)


def tags_generator():
    response = []
    count = random.randint(3, 8)
    for _ in range(count):
        length = random.randint(2, 4)
        t = ''.join(random.choice(alphabet) for i in range(length))
        response.append(t)
    return response


def restaurant_generator() -> dict:
    longitude = ".".join([str(random.randint(0, 360)), str(random.randint(100000, 900000))])
    latitude = ".".join([str(random.randint(0, 180) - 90), str(random.randint(100000, 900000))])
    address_line_1 = ''.join(
        random.choice(alphabet) for i in range(random.randint(5, 15))
    ).capitalize() + " street " + str(random.randint(1, 150))

    res = dict()
    res['name'] = name_generator()
    res['country'] = random.choice(["Germany", "US", "Austria", "Italy", "France"])
    res['city'] = "City-" + str(random.randint(100, 100000))
    res['zip_code'] = str(random.randint(10000, 99999))
    res['address_line_1'] = address_line_1
    res['cuisine'] = random.choice(cuisine_values)
    res['longitude'] = longitude
    res['latitude'] = latitude
    res['service_type'] = random.choice(service_type_values)
    res['web_address'] = "www.example.com"
    res['tags'] = tags_generator()
    return res
