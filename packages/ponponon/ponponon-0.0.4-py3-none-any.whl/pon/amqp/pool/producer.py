from kombu.messaging import Producer
from kombu.pools import producers, ProducerPool
from kombu import Connection, Producer


def get_producer_pool(connection: Connection) -> ProducerPool:
    producer_pool: ProducerPool = producers[connection]
    return producer_pool


def get_producer_from_pool(pool: ProducerPool) -> Producer:
    return pool.acquire(block=True)


def get_producer_from_pool_group(connection: Connection) -> Producer:
    return get_producer_from_pool(get_producer_pool(connection))
