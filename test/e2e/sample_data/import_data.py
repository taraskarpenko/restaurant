from concurrent.futures.thread import ThreadPoolExecutor

import requests

from test.e2e.sample_data.data import restaurant_generator


def import_restaurant():
    payload = restaurant_generator()
    res = requests.post(url="http://127.0.0.1:5000/restaurant", json=payload)
    return res.json()['id']


def import_restaurants(qty=10):
    futures = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(qty):
            future = executor.submit(import_restaurant)
            futures.append(future)
    return [f.result() for f in futures]


if __name__ == "__main__":
    import_restaurants(10)
