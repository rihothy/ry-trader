from threading import Lock
import copy
import json

lock = Lock()
data = json.load(open('config.json'))

def get():
    with lock:
        return copy.deepcopy(data)


def put(key, val):
    with lock:
        data[key] = val
        json.dump(data, open('config.json', 'w'), indent=4)