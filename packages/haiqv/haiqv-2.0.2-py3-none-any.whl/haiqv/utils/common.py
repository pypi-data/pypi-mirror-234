import time
import socket


def get_millis():
    return int(time.time() * 1000)


def key_subset_split(key):
    split = key.split('/')
    return split if len(split) > 1 else (key, None)


def get_ip():
    try:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except Exception as e:
        print('cannot get IP information: ', str(e))
        return None
