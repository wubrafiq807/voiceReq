import json


class JsonSerializable(object):
    def toJson(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.toJson()


class Utility(JsonSerializable):
    def __init__(self, result = object, error=False, message=''):
        self.result=result
        self.error=error
        self.message=message