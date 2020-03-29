import json
from concurrent.futures.thread import ThreadPoolExecutor

import requests

from test.e2e.sample_data.data import restaurant_generator


def import_restaurant():
    payload = restaurant_generator()
    res = requests.post(url="http://127.0.0.1:5000/restaurant", json=payload)
    print(res)


if __name__ == "__main__":
    futures = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        for _ in range(10):
            future = executor.submit(import_restaurant)
            futures.append(future)
    [f.result() for f in futures]
