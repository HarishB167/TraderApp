import json
import os
from json.decoder import JSONDecodeError

from . import constants as c


def save_broker_data(key, value):    
    if not os.path.exists(c.DATA_FOLDER):
        os.makedirs(c.DATA_FOLDER)
    filepath = os.path.join(c.DATA_FOLDER, c.BROKER_INFO_FILE)

    # with open(filepath, 'r') as file:
    #     data = file.read()
    #     try:
    #         obj = json.loads(data)
    #     except JSONDecodeError:
    #         obj = {}
    obj = load_broker_data()    
    if obj is None:
        obj = {}

    with open(filepath, 'w+') as file:            
        obj[key] = value
        json.dump(obj, file, indent=4)

def load_broker_data():  
    if os.path.exists(c.DATA_FOLDER):
        filepath = os.path.join(c.DATA_FOLDER, c.BROKER_INFO_FILE)
        with open(filepath, 'r') as file:
            data = file.read()
            try:
                obj = json.loads(data)
                return obj
            except JSONDecodeError:
                print("Broker info file is not in JSON format.")
                return None
    print("Broker info file doesn't exist.")
    return None
    