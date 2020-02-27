import json


class categoria:
    def __init__(self, jsonreq):
        self.__dict__ = json.loads(jsonreq)