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
                 partition: str='',
                 root='root',
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
        self.root=root
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
        return ':'.join(folder for folder in [self.root,self.domain, self.category, self.partition] if folder)
    @property
    def incr(self):
        """
        Computes the increment value associated with the category using the engine's 'incr' method.
        
        Returns:
            int: The increment value.
        """
        return self.engine.incr('items')
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
        return flatten_dict(data.to_dict())
    def push(self,result):
        """
        Pushes a mapped data object to the Redis database.
        Args:
            result: The mapped data object to push to Redis.
        Returns:
            None
        """
        self.engine.hset(self.id,mapping=self.pipe(result))
class RedisUser(Redis):
    def users_pattern(self,tel):
        return ':'.join([
            self.root,
            'Users',
            tel,
            'Domains',
            self.domain,
            'Categories',
            self.category])
    def push(self,result):
        piped = self.pipe(result)
        tel_id = self.tel_id(piped['Contact'])
        title = piped['ProductTitle']
        pattern = self.users_pattern(tel_id)
        incr = self.engine.incr(pattern)
        id = f'{pattern}:{title}:{incr}'
        self.engine.hset(id,mapping=piped)
    def parent_tel_pattern(self,tel,parent):
        return f'{self.root}:Ids:{parent}:{tel}'
    def set_parent(self,tel,parent):
        pattern = self.parent_tel_pattern(tel,parent)
        self.engine.set(pattern,tel)
        return pattern
    def get_tel_parent(self,tel):
        old = self.engine.keys(pattern=f'{self.root}:Ids:*:{tel}')
        if not old:
            old = [self.set_parent(tel,tel)]
        return old
    def update_tel_parent(self,tel,old_parent,parent):
        self.engine.delete(old_parent[0])
        return self.set_parent(tel,parent)
    def tel_id(self,tel):
        tels = tel.split(';')
        tel = 'Unknown'
        if tels[0]:
            parents = [self.get_tel_parent(tel) for tel in tels ]
            tel = parents.pop()[0].split(':')[2]
            for other,old_parent in zip(tels,parents):
                self.update_tel_parent(other,old_parent,tel)
        return tel