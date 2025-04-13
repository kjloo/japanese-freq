from flask.json.provider import DefaultJSONProvider
import json

from app.module.logging_module import logger


def _encode_with_to_dict(obj, parent_default):
    """
    Utility function to handle objects with a `to_dict` method.
    Falls back to the parent class's `default` method if `to_dict` is not available.
    """
    logger.debug("Encoding object of type %s", type(obj))
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return parent_default(obj)


# Custom JSON Encoder for json.dumps
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return _encode_with_to_dict(obj, super().default)


# Custom JSON Provider for Flask
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        return _encode_with_to_dict(obj, super().default)
