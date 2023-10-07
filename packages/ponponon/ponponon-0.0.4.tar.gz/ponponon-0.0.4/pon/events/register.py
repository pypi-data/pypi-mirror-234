from functools import wraps
from typing import Callable,Dict
from loguru import logger


PON_METHOD_ATTR_NAME = 'pon_consumer_func_config'

PON_CONSUMER_METHODS: Dict[type, Callable] = {}


def event_handler(source_service: str, event_name: str, **event_handler_kwagrs):
    def decorate(pon_service_cls_consumer_method: Callable):

        pon_consumer_func_config = {
            'source_service': source_service,
            'event_name': event_name
        }

        pon_consumer_func_config.update(event_handler_kwagrs)

        if not hasattr(pon_service_cls_consumer_method, PON_METHOD_ATTR_NAME):
            setattr(
                pon_service_cls_consumer_method,
                PON_METHOD_ATTR_NAME,
                pon_consumer_func_config
            )

        @wraps(pon_service_cls_consumer_method)
        def wrapper(*args, **kwargs):
            return pon_service_cls_consumer_method(*args, **kwargs)
        return wrapper
    return decorate
