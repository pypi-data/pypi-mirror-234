import os
import sys
from pathlib import Path
from typing import Tuple, ClassVar, Type, Dict, List, Callable, Any
import yaml
import inspect
from loguru import logger
from kombu import Exchange, Queue
from kombu.utils.compat import nested
from kombu import Connection, Consumer, Queue
from kombu.transport.pyamqp import Channel
from pon.events.message import MessageConsumer
from pon.standalone.events import get_event_exchange
from pon.core import get_class_names
from pon.events.register import event_handler


def is_dispatcher(obj: Type[Any]) -> bool:
    return isinstance(obj, EventDispatcher)


class EventRunnerContext:
    service_name: str

    def __init__(self, config: dict):
        self.config = config

    def setup_service_name(self, service_name: str):
        self.service_name: str = service_name


class EventDispatcher:
    context: EventRunnerContext

    def __call__(self, event_type: str, event_data: Any) -> None:
        from pon.standalone.events import event_dispatcher
        amqp_uri = self.context.config['AMQP_URI']
        dispatch = event_dispatcher(amqp_uri)
        dispatch(
            service_name=self.context.service_name,
            event_type=event_type,
            event_data=event_data
        )


class QueueLine:
    queue: Queue
    service_cls: Type
    method: Callable

    def __init__(self, queue: Queue, service_cls: Type, method: Callable) -> None:
        self.queue = queue
        self.service_cls = service_cls
        self.method = method


class EventletEventRunner:
    amqp_uri: str
    queues: List[QueueLine]

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
                raise Exception(f'Wrong service format: {service}')

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
        logger.info(self.amqp_uri)

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

        self.queues: List[QueueLine] = []

        service_cls_list: List[type] = self.load_service_cls_list(services)

        from pon.events.register import PON_METHOD_ATTR_NAME
        # 1. 去 rabbitmq 创建消息队列

        pon_service_cls_list: List[type] = []

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
                if hasattr(cls_property, PON_METHOD_ATTR_NAME):

                    pon_service_cls_list.append(service_cls)

                    consumer_method = cls_property
                    pon_consumer_func_config = getattr(
                        consumer_method, PON_METHOD_ATTR_NAME)
                    # 获取修饰器附加的参数
                    source_service: str = pon_consumer_func_config['source_service']
                    event_name: str = pon_consumer_func_config['event_name']

                    exchange_name = get_event_exchange(
                        source_service).name
                    routing_key: str = event_name

                    exchange = Exchange(exchange_name, type='topic')

                    self.declare_exchange(exchange)

                    queue_name = f'evt-{exchange_name}-{routing_key}--{service_cls.name}.{consumer_method.__name__}'

                    queue = Queue(queue_name, exchange,
                                  routing_key, durable=True, queue_arguments={'x-max-priority': 10})
                    self.declare_queue(queue)
                    self.queues.append(QueueLine(
                        queue, service_cls, consumer_method))

        logger.info(
            f'load services: {", ".join([sc.__name__ for sc in set(pon_service_cls_list)])}')

        # 2. 开始监听和消费
        while True:
            try:
                from pon.constants import DEFAULT_FRAMEWORK, DEFAULT_FRAMEWORK_GITHUB, DEFAULT_PROJECT_NAME
                from pon import VERSION
                framework = self.context.config.get(
                    'FRAMEWORK', DEFAULT_FRAMEWORK)
                framework_github = self.context.config.get(
                    'DEFAULT_FRAMEWORK_GITHUB', DEFAULT_FRAMEWORK_GITHUB)
                project_name = self.context.config.get(
                    'PROJECT_NAME', os.environ['PROJECT_NAME'] or DEFAULT_PROJECT_NAME)

                with Connection(self.amqp_uri, transport_options={
                        'client_properties': {
                            'framework': framework,
                            'framework_version': VERSION,
                            'framework_github': framework_github,
                            'project_name': project_name,
                        }}) as conn:
                    consumers: List[Consumer] = []
                    for queueline in self.queues:

                        channel: Channel = conn.channel()
                        consumer = Consumer(
                            channel,
                            queues=[queueline.queue],
                            prefetch_count=10,
                            on_message=MessageConsumer(
                                queue=queueline.queue,
                                service_cls=queueline.service_cls,
                                consumer_method=queueline.method
                            ).handle_message
                        )
                        consumers.append(consumer)
                    logger.info(f'start consuming {self.amqp_uri}')

                    with nested(*consumers):
                        while True:
                            conn.drain_events()
            except Exception as error:
                logger.warning(error)
