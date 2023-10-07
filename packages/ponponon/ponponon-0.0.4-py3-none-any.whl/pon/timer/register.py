from functools import wraps
from typing import Callable, Dict, Union, Any

PON_TIMER_METHOD_ATTR_NAME = 'pon_timer_func_config'


def timer(interval: Union[int, float]):
    def decorate(pon_service_cls_timer_method: Callable):

        pon_timer_func_config: Dict[str, Any] = {
            'interval': interval,
        }

        if not hasattr(pon_service_cls_timer_method, PON_TIMER_METHOD_ATTR_NAME):
            setattr(
                pon_service_cls_timer_method,
                PON_TIMER_METHOD_ATTR_NAME,
                pon_timer_func_config
            )

        @wraps(pon_service_cls_timer_method)
        def wrapper(*args, **kwargs):
            return pon_service_cls_timer_method(*args, **kwargs)
        return wrapper
    return decorate
