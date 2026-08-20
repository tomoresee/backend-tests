import json


class JsonUtils:
    @staticmethod
    def is_json(obj: str) -> bool:
        try:
            json.loads(obj)
        except ValueError:
            return False
        return True
