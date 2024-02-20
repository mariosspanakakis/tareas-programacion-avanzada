import json
from os.path import join

# accesar data del archivo 'parametros.json'
def data_json(key):
    path = join("parametros.json")
    with open(path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    value = data[key]
    return value