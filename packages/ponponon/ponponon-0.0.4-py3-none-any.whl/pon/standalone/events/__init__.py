from typing import Union, Dict
from kombu import Exchange
from kombu import Connection
from kombu.messaging import Producer
from kombu.transport.base import Message

from kombu import Exchange, Queue
from loguru import logger
import time
from pon.constants import NON_PERSISTENT, PERSISTENT


def get_event_exchange(service_name: str) -> Exchange:
    exchange_name = "{}.events".format(service_name)
    exchange = Exchange(
        exchange_name,
        type='topic',
        durable=True,
        delivery_mode=PERSISTENT,
        auto_delete=False,
        no_declare=False,
    )

    return exchange


def event_dispatcher(amqp_uri: str, **default_kwargs):
    from pon.amqp.pool.producer import get_producer_from_pool_group

    def dispatch(service_name: str, event_type: str, event_data: Union[str, bytes, Dict], **kwargs):
        default_kwargs.update(kwargs)
        """ Dispatch an event claiming to originate from `service_name` with
        the given `event_type` and `event_data`.
        """
        exchange = get_event_exchange(service_name)
        routing_key: str = event_type

        with get_producer_from_pool_group(Connection(amqp_uri)) as producer:
            message = Message(body=event_data)
            producer.publish(
                body=message.body,
                exchange=exchange,
                routing_key=routing_key,
                **default_kwargs  # TODO args safe
            )
    return dispatch
