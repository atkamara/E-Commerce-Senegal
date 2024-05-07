"""Con.py - Module for Redis Cursor Objects
This module provides Cursor objects for interacting with Redis database.
Classes:
    Redis: Cursor object for Redis operations.
    RedisUser: Cursor object for Redis operations specific to users.
Usage:
    Typical usage involves creating an instance of Redis or RedisUser and using its methods for database operations.
Example:
    # Import Con module
    from .Con import Redis, RedisUser
    # Create Redis instance
    redis_instance = Redis(domain="example", category="test")
    # Get pattern
    pattern = redis_instance.pattern
    # Increment value
    incr_value = redis_instance.incr
    # Get id
    id_value = redis_instance.id
    # Push data
    result_data = {"key1": "value1", "key2": "value2"}
    redis_instance.push(result_data)
    # Create RedisUser instance
    redis_user_instance = RedisUser(domain="example", category="test")
    # Get users pattern
    users_pattern = redis_user_instance.users_pattern("1234567890")
    # Push data for user
    result_data_user = {"Contact": "1234567890", "ProductTitle": "Example Product"}
    redis_user_instance.push(result_data_user)
    # Set parent
    redis_user_instance.set_parent("1234567890", "parent")
    # Get tel parent
    tel_parent = redis_user_instance.get_tel_parent("1234567890")
    # Update tel parent
    updated_tel_parent = redis_user_instance.update_tel_parent("1234567890", tel_parent, "new_parent")
    # Get tel id
    tel_id = redis_user_instance.tel_id("1234567890")
"""
import redis
from .Model import Cursor
from .utils import flatten_dict
class Redis(Cursor):
    """Cursor object for Redis operations."""
    def __init__(self,
                 domain: str,
                 category: str,
                 partition: str = '',
                 root: str = 'root',
                 **kwargs) -> None:
        """
        Initialize Redis Cursor.
        Args:
            domain (str): Domain value.
            category (str): Category value.
            partition (str, optional): Partition value. Defaults to ''.
            root (str, optional): Root value. Defaults to 'root'.
            **kwargs: Additional keyword arguments for redis.Redis.
        Attributes:
            root (str): Root value.
            domain (str): Domain value.
            category (str): Category value.
            partition (str): Partition value.
            engine: Redis engine.
        """
        self.root = root
        self.domain = domain
        self.category = category
        self.partition = partition
        self.engine = redis.Redis(**kwargs)
    @property
    def pattern(self):
        """Get pattern."""
        return ':'.join(folder for folder in [self.root, self.domain, self.category, self.partition] if folder)
    @property
    def incr(self):
        """Get increment value."""
        return self.engine.incr('items')
    @property
    def id(self):
        """Get id."""
        return f'{self.pattern}:{self.incr}'
    def pipe(self, data):
        """Pipe data."""
        return flatten_dict(data.to_dict())
    def push(self, result):
        """Push data."""
        self.engine.hset(self.id, mapping=self.pipe(result))
class RedisUser(Redis):
    """Cursor object for Redis operations specific to users."""
    def users_pattern(self, tel):
        """Get users pattern."""
        return ':'.join([
            self.root,
            'Users',
            tel,
            'Domains',
            self.domain,
            'Categories',
            self.category
        ])
    def push(self, result):
        """Push data for user."""
        piped = self.pipe(result)
        tel_id = self.tel_id(piped['Contact'])
        title = piped['ProductTitle']
        pattern = self.users_pattern(tel_id)
        incr = self.engine.incr(pattern)
        id = f'{pattern}:{title}:{incr}'
        self.engine.hset(id, mapping=piped)
    def parent_tel_pattern(self, tel, parent):
        """Get parent tel pattern."""
        return f'{self.root}:Ids:{parent}:{tel}'
    def set_parent(self, tel, parent):
        """Set parent."""
        pattern = self.parent_tel_pattern(tel, parent)
        self.engine.set(pattern, tel)
        return pattern
    def get_tel_parent(self, tel):
        """Get tel parent."""
        old = self.engine.keys(pattern=f'{self.root}:Ids:*:{tel}')
        if not old:
            old = [self.set_parent(tel, tel)]
        return old
    def update_tel_parent(self, tel, old_parent, parent):
        """Update tel parent."""
        self.engine.delete(old_parent[0])
        return self.set_parent(tel, parent)
    def tel_id(self, tel):
        """Get tel id."""
        tels = tel.split(';')
        tel = 'Unknown'
        if tels[0]:
            parents = [self.get_tel_parent(tel) for tel in tels]
            tel = parents.pop()[0].split(':')[2]
            for other, old_parent in zip(tels, parents):
                self.update_tel_parent(other, old_parent, tel)
        return tel
