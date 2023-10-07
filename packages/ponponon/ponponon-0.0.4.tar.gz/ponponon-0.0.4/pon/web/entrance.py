from functools import wraps
from typing import Callable, List
from werkzeug.routing import Map, Rule


url_map = Map()


def http(methods: List[str], url: str):
    def decorate(service_cls_api_method: Callable):
        url_map.add(Rule(
            url, endpoint=service_cls_api_method
        ))

        @wraps(service_cls_api_method)
        def wrapper(*args, **kwargs):
            return service_cls_api_method(*args, **kwargs)
        return wrapper
    return decorate
