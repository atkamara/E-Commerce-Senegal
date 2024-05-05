"""
Provides a Redis connection interface.
This module defines the Redis class, which serves as a connection interface 
for interacting with a Redis database.
Classes:
    Redis: Represents a connection to a Redis database.
Functions:
    flatten_dict: Flatten a dictionary with nested dictionaries and lists.
"""
from .Model import Con 
import redis
from .utils import flatten_dict
class Redis(Con):
    """
    Represents a connection to a Redis database.
    Attributes:
        category (str): The category for the Redis data.
        partition (str): The partition for the Redis data.
        engine: The Redis connection object.
    Methods:
        __init__: Initializes a Redis object with the provided parameters.
        Push: Pushes a mapped data object to the Redis database.
    """
    def __init__(self,
                 category,
                 partition: str,
                 host: str,
                 port: int = 6379,
                 username: str = ...,
                 password: str = ...,
                 **kwargs) -> None:
        """
        Initializes a Redis object with the provided parameters.
        Args:
            category (str): The category for the Redis data.
            partition (str): The partition for the Redis data.
            host (str): The hostname or IP address of the Redis server.
            port (int, optional): The port number of the Redis server. Defaults to 6379.
            username (str, optional): The username for Redis authentication. Defaults to None.
            password (str, optional): The password for Redis authentication. Defaults to None.
            **kwargs: Additional keyword arguments passed to the Redis connection.
        Returns:
            None
        """
        self.category = category
        self.partition = partition
        self.engine = redis.Redis(host, port, username, password, **kwargs)
    def Push(MappedData):
        """
        Pushes a mapped data object to the Redis database.
        Args:
            MappedData: The mapped data object to push to Redis.
        Returns:
            None
        """
        incr = self.engine.incr(self.category)
        self.engine.hset(f'{self.category}:{self.partition}:{incr}',
                         mapping=flatten_dict(str(MappedData)))