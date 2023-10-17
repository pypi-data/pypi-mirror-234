import json


def join_threads(threads):
    for t in threads:
        t.join(timeout=1)


def send_json(json_val):
    return json.dumps(json_val).encode()


def recv_json(byte_val):
    return json.loads(byte_val.decode())


def to_tuple(json_data):
    temp_list = []
    for i in json_data:
        temp_list.append(tuple(i))
    return temp_list
