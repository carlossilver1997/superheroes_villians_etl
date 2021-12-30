import json
__config = None

def config():
    global __config
    if not __config:
        with open('config.json', mode='r') as f:
            __config = json.load(f)
    return __config