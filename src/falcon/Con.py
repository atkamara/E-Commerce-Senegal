"""
Provides a Redis connection interface.
This module defines the Redis class, which serves as a connection interface 
for interacting with a Redis database.
Classes:
    Redis: Represents a connection to a Redis database.
Functions:
    flatten_dict: Flatten a dictionary with nested dictionaries and lists.
"""
import redis
from .Model import Cursor
from .utils import flatten_dict
class Redis(Cursor):
    """
    Represents a connection to a Redis database.
    Attributes:
        category (str): The category for the Redis data.
        partition (str): The partition for the Redis data.
        engine: The Redis connection object.
    Methods:
        __init__: Initializes a Redis object with the provided parameters.
        push: Pushes a mapped data object to the Redis database.
    """
    def __init__(self,
                 domain:str,
                 category : str,
                 partition: str,
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
        self.engine = redis.Redis(**kwargs)
    @property
    def pattern(self):
        """
        Generates a pattern based on the domain, category, and partition attributes.
        
        Returns:
            str: The generated pattern, where non-empty attributes are joined with a colon (':').
        """
        return ':'.join(folder for folder in [self.domain, self.category, self.partition] if folder)
    @property
    def incr(self):
        """
        Computes the increment value associated with the category using the engine's 'incr' method.
        
        Returns:
            int: The increment value.
        """
        return self.engine.incr(self.category)
    @property
    def id(self):
        """
        Generates an ID based on the pattern and increment values.
        
        Returns:
            str: The generated ID, formatted as 'pattern:incr'.
        """
        return f'{self.pattern}:{self.incr}'
    def pipe(self, data):
        """
        Processes the input data and returns a flattened string representation.
        
        Args:
            data: Input data to be processed.
        Returns:
            str: Flattened string representation of the input data.
        """
        return flatten_dict(str(data))
    def push(self,result):
        """
        Pushes a mapped data object to the Redis database.
        Args:
            result: The mapped data object to push to Redis.
        Returns:
            None
        """
        self.engine.hset(self.id,
                         mapping=self.pipe(result))
