import json


class Json:
    @staticmethod
    def read(path):
        with open(path, encoding="utf8") as json_file:
            return json.load(json_file)

    @staticmethod
    def write(path, data):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(Json.dumps(data))

    @staticmethod
    def print(data):
        print(Json.dumps(data))

    @staticmethod
    def dumps(data, indent=2, ensure_ascii=False):
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)
