from flask.json.provider import DefaultJSONProvider


class JSONProvider(DefaultJSONProvider):
    ensure_ascii = False
