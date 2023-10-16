import json
from jsonpath_ng import jsonpath, parse


class Context:
    def get_id(self) -> str:
        pass

    def set(self, key: str, value: object):
        pass

    def get(self, key: str) -> object:
        pass

    def get_raw(self) -> bytes:
        pass

    def set_raw(self, data: bytes):
        pass

    def is_empty(self) -> bool:
        pass


class Message(Context):
    def __init__(self, data: bytes):
        msg = json.loads(data.decode("utf-8"))
        self.id = msg["id"]
        self.data = data

    def get_id(self) -> str:
        return str(self.id)

    def set(self, key: str, value: object):
        msg = json.loads(self.data.decode("utf-8"))
        msg[key] = value
        self.data = json.dumps(msg).encode("utf-8")

    def get(self, key: str) -> object:
        msg = json.loads(self.data.decode("utf-8"))
        val = parse("$.%s" % key).find(msg)
        if len(val) == 0:
            return None

        return val[0].value

    def get_raw(self) -> bytes:
        return self.data

    def set_raw(self, data: bytes):
        self.data = data

    def is_empty(self) -> bool:
        return self.data == None or len(self.data) == 0
