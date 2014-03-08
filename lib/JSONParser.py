import json

class JSONParser:

    @staticmethod
    def Parse(JSON):
        res = json.loads(JSON)
        return res
