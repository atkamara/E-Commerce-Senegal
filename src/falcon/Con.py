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
from functools import cached_property
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
                 domain:str,
                 category : str,
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
        self.domain = domain
        self.category = category
        self.partition = partition
        self.engine = redis.Redis(host, port, username, password, **kwargs)
    @cached_property
    def pattern(self):
        return ':'.join(folder for folder in [self.domain,self.category,self.partition] if folder)
    @property
    def incr(self):
        return self.engine.incr(self.category)
    @property
    def id(self):
        f'{self.pattern}:{self.incr}'
    def pipe(self,data):
        return flatten_dict(str(data))
    def Push(MappedData):
        """
        Pushes a mapped data object to the Redis database.
        Args:
            MappedData: The mapped data object to push to Redis.
        Returns:
            None
        """
        self.engine.hset(self.id,
                         mapping=self.pipe(MappedData))