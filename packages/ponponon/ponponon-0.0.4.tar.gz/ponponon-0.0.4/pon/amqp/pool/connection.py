from kombu import Connection
from kombu.pools import connections
from kombu.connection import ConnectionPool
from kombu import Connection


def get_connection_pool(connection: Connection) -> ConnectionPool:
    """
    connections 是 Connections 的实例, Connections 是 PoolGroup 的子类
    """
    connection_pool: ConnectionPool = connections[connection]
    return connection_pool


def get_connection_from_pool(pool: ConnectionPool) -> Connection:
    return pool.acquire(block=True)


def get_connection_from_pool_group(connection: Connection) -> Connection:
    return get_connection_from_pool(get_connection_pool(connection))
