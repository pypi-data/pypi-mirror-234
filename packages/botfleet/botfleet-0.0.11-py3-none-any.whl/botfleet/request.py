import os
import json
from copy import deepcopy


class QueryDict:
    def __init__(self, data):
        self.data = {k: v for k, v in deepcopy(data).items() if len(v) > 0}

    def __repr__(self):
        return f"<QueryDict: {self.data}>"

    def __getitem__(self, key):
        return self.data[key][-1]

    def __contains__(self, key):
        return key in self.data

    def get(self, key, default=None):
        if key not in self.data:
            return default
        return self.__getitem__(key)

    def getlist(self, key, default=None):
        if key not in self.data:
            return default
        return self.data[key]


class Request:
    def __init__(self):
        GET = os.getenv("__BOTFLEET__GET", None)
        POST = os.getenv("__BOTFLEET__POST", None)
        self.method = "GET" if GET is not None else "POST"
        self.GET = QueryDict(json.loads(GET) if GET is not None else {})
        self.POST = json.loads(POST) if POST is not None else {}
