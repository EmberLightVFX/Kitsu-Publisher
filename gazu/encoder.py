import json
import datetime


class CustomJSONEncoder(json.JSONEncoder):
***REMOVED***
    This JSON encoder is here to handle dates which are not handled by default.
    The standard does not want to assum how you handle dates.
***REMOVED***

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
***REMOVED*** obj.isoformat()

        return json.JSONEncoder.default(self, obj)
