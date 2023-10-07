import os
import sys
from pathlib import Path
from typing import Tuple, ClassVar, Type, Dict, List, Callable, Any, Union
import yaml
import inspect
from loguru import logger
from kombu import Exchange, Queue
from kombu.utils.compat import nested
from kombu import Connection, Consumer, Queue
from kombu.transport.pyamqp import Channel
from pon.timer.register import timer
from pon.events.message import MessageConsumer
from pon.standalone.events import get_event_exchange
from pon.core import get_class_names
from pon.events.register import event_handler
from pon.events import is_dispatcher, EventRunnerContext, EventDispatcher
from pon.timer.register import PON_TIMER_METHOD_ATTR_NAME


class EventletTimerRunner:
    amqp_uri: str

    def __init__(self) -> None:
        self.put_patch()

    def put_patch(self) -> None:
        import eventlet
        eventlet.monkey_patch()  # noqa (code before rest of imports)

    def load_service_cls_list(self, services: Tuple[str]) -> List[type]:
        BASE_DIR: Path = Path(os.getcwd())
        sys.path.append(str(BASE_DIR))

        service_cls_list: List[type] = []

        for service in services:
            items: List[str] = service.split(':')
            if len(items) == 1:
                module_name, service_class_name = items[0], None
            elif len(items) == 2:
                module_name, service_class_name = items
            else:
                raise Exception(f'错误的 service 格式: {service}')

            __import__(module_name)
            module = sys.modules[module_name]

            if service_class_name:
                service_class_names = [service_class_name]
            else:
                service_class_names = get_class_names(module_name)

            for service_class_name in service_class_names:
                service_cls = getattr(module, service_class_name)
                service_cls_list.append(service_cls)

        return service_cls_list

    def load_config(self, config_filepath: Path):
        with open(config_filepath, 'r', encoding='utf-8') as f:
            config: Dict[str, Dict] = yaml.safe_load(f)
            self.context = EventRunnerContext(config)
        self.amqp_uri = config['AMQP_URI']

    def declare_exchange(self, exchange: Exchange):
        with Connection(self.amqp_uri) as conn:
            with conn.channel() as channel:
                exchange.declare(channel=channel)

    def declare_queue(self, queue: Queue):
        with Connection(self.amqp_uri) as conn:
            with conn.channel() as channel:
                queue.declare(channel=channel)

    def run(self, services: Tuple[str], config_filepath: Path):
        self.load_config(config_filepath)

        service_cls_list: List[type] = self.load_service_cls_list(services)

        from pon.events.register import PON_METHOD_ATTR_NAME
        # 1. 去 rabbitmq 创建消息队列

        for service_cls in service_cls_list:
            for attr_name, dispatcher in inspect.getmembers(
                    service_cls,
                    is_dispatcher
            ):
                dispatcher: EventDispatcher
                dispatcher.context = self.context
                dispatcher.context.setup_service_name(service_cls.name)

            for item in dir(service_cls):
                cls_property: Callable = getattr(service_cls, item)
                if hasattr(cls_property, PON_TIMER_METHOD_ATTR_NAME):
                    consumer_method = cls_property

                    pon_timer_func_config = getattr(
                        consumer_method, PON_TIMER_METHOD_ATTR_NAME)
                    # 获取修饰器附加的参数
                    interval: Union[int,
                                    float] = pon_timer_func_config['interval']
                    service_instance = service_cls()
                    consumer_method(service_instance, interval)
