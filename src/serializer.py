import json
from collections import namedtuple


class Serializer(object):
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @staticmethod
    def from_json(json_data):
        return json.loads(json_data, object_hook=Serializer.custom_decoder)

    @staticmethod
    def custom_decoder(json_obj):
        return namedtuple('custom_decoded', json_obj.keys())(*json_obj.values())
