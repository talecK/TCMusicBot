import json
from api import api_v1
from flask import request
from datetime import datetime
from bson.objectid import ObjectId

class APIConverter(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        elif isinstance(obj, ObjectId):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

def json_response(*args, **kwargs):
    return api_v1.response_class(json.dumps(dict(*args, **kwargs), cls=APIConverter,
        indent=None if request.is_xhr else 2), mimetype="application/json")
