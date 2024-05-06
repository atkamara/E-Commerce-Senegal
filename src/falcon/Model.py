"""
Main module containing classes for web scraping and data formatting.
Classes:
    Formatter: Abstract base class representing a data formatter.
    Field: A class representing a field extracted from HTML content.
    Item: A class representing an item extracted from a web page.
    Config: A class for reading and accessing configuration settings.
    Page: Abstract base class representing a web page.
    Site: A class representing a website for web scraping.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from functools import wraps, cached_property
from dataclasses import asdict, make_dataclass
from datetime import datetime
import configparser
import logging
from scrapy import Spider
logger = logging.getLogger()
class ParseError(BaseException):
    """
    Exception raised when parsing encounters an error.
    This exception is raised when there is an error during parsing of data,
    such as invalid format or missing required fields.
    Attributes:
        message (str): Optional error message describing the parsing error.
    Methods:
        __init__(self, message=None): Initializes a ParseError instance with an optional error message.
        __str__(self): Returns a string representation of the exception.
    Examples:
        >>> raise ParseError("Invalid data format")
        Traceback (most recent call last):
            ...
        ParseError: Invalid data format
    """
class Formatter(ABC):
    """
    Abstract base class representing a data formatter.
    Methods:
        cast: Static method to cast values with error handling.
        fmethod: Abstract method defining the formatting behavior.
        Format: Formats the given value using the specified formatting method.
    """
    @staticmethod
    def cast(func) -> callable:
        """
        Static method to cast values with error handling.
        Args:
            func: The formatting function.
        Returns:
            callable: A wrapped function with error handling.
        """
        @wraps(func)
        def wrapper(self, value: str):
            """
            Wrapper function with error handling for formatting.
            Args:
                self: The instance of the class.
                value (str): The value to format.
            Returns:
                Any: The formatted value, or None if formatting fails.
            """
            res = None
            try:
                res = func(self, value)
            except ParseError:
                logger.warning('failed parsing %s'%value)
            return res
        return wrapper
    @abstractmethod
    def fmethod(self, value):
        """
        Abstract method defining the formatting behavior.
        Args:
            value: The value to format.
        Returns:
            Any: The formatted value.
        """
    @cast
    def format(self, value):
        """
        Formats the given value using the specified formatting method.
        Args:
            value: The value to format.
        Returns:
            Any: The formatted value.
        """
        return self.fmethod(value)
class Field(Formatter):
    """
    A class representing a field extracted from HTML content.
    Attributes:
        xpaths (list): A list of XPath expressions to extract values.
        relative_xpaths (list): A list of XPath expressions relative to the current element.
        regex_list (list): A list of regular expressions to match values.
    Methods:
        __init__: Initializes a Field object with the provided HTML content.
        getter: Retrieves values from HTML content based on specified paths.
        value: Property returning values extracted using xpaths.
        relative_value: Property returning values extracted using relative_xpaths.
    """
    xpaths: list[str]
    relative_xpaths: list[str]
    regex_list: list[str]
    def __init__(self, html):
        """
        Initializes a Field object with the provided HTML content.
        Args:
            html: The HTML content from which to extract values.
        """
        self.html = html
    def getter(self, paths='xpaths')->list:
        """
        Retrieves values from HTML content based on specified paths.
        Args:
            paths (str): The type of paths to use for extraction. Defaults to 'xpaths'.
        Returns:
            list: A list of extracted values.
        """
        out = self.html.xpath('|'.join(getattr(self,paths))).getall()
        return self.format(out)
    @cached_property
    def value(self):
        """
        Property returning values extracted using xpaths.
        Returns:
            list: A list of extracted values.
        """
        return self.getter(paths='xpaths')
    @cached_property
    def relative_value(self):
        """
        Property returning values extracted using relative_xpaths.
        Returns:
            list: A list of extracted values.
        """
        return self.getter(paths='relative_xpaths')
class Cursor(ABC):
    """
    Abstract base class representing a connection interface.
    Methods:
        push: Abstract method to push an object to the connection.
    """
    def __bool__(self):
        return True
    @abstractmethod
    def push(self,result):
        """
        Abstract method to push an object to the connection.
        Args:
            result: The object to push to the connection.
        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
class MappedData:
    """
    Represents mapped data with a specific name and fields.
    Attributes:
        name (str): The name of the mapped data.
        fields (list): A list of field names for the dataclass.
        dataclass: The constructed dataclass object representing the mapped data.
    Methods:
        __init__: Initializes a MappedData object with the provided name and fields.
        __str__: Returns the dataclass as a dictionary.
        __rshift__: Pushes the string representation of the dataclass to a consumer.
    """
    def __init__(self, name, fields):
        """
        Initializes a MappedData object with the provided name and fields.
        Args:
            name (str): The name of the mapped data.
            fields (list): A list of field names for the dataclass.
        """
        self.name = name
        self.fields = fields
        self.dataclass = make_dataclass(self.name, self.fields)()
    def to_dict(self):
        """
        Returns the dataclass as a dictionary.
        Returns:
            dict: The dataclass represented as a dictionary.
        """
        return asdict(self.dataclass)
    def __rshift__(self, cursor):
        """
        Pushes the string representation of the dataclass to a consumer.
        Args:
            cursor: The consumer object to which the data is pushed.
        """
        cursor.push(self)
class Item:
    """
    A class representing an item extracted from a web page.
    Methods:
        register: Registers a fieldclass to the Item class.
        __str__: Returns the name of the Item class as a string.
        __rshift__: Defines the behavior for the '>>' operator.
        parse: Parses HTML content and constructs an Item object.
    """
    @classmethod
    def register(cls, fieldclass) -> None:
        """
        Registers a fieldclass to the Item class.
        Args:
            fieldclass: The class representing a field in the Item.
        Returns:
            None
        """
        if not hasattr(cls, 'registry'):
            cls.registry: set = set()
        cls.registry.add(fieldclass)
    def __str__(self):
        """
        Returns the name of the Item class as a string.
        Returns:
            str: The name of the Item class.
        """
        return self.__class__.__name__
    @classmethod
    def parse(cls, html, method='value'):
        """
        Parses HTML content and constructs an Item object.
        Args:
            html: HTML content to parse.
            method (str, optional): The parsing method. Defaults to 'value'.
        Returns:
            dataclass: The constructed dataclass object representing the parsed item.
        """
        self = cls()
        item_fields = [
            (field.__name__,
             field.fmethod.__annotations__.get('return', str).__name__,
             getattr(field(html), method))
            for field in self.registry
        ] + [('CreatedAt', datetime, datetime.now().isoformat())]
        return MappedData(str(self), item_fields)
class Config:
    """
    A class for reading and accessing configuration settings.
    Attributes:
        _conf_file (str): The path to the configuration file.
        _val_conf_attr (list): A list of valid configuration attributes.
        check_stage (int): The stage of attribute checking.
    Methods:
        read_conf: Property to read the configuration file.
    """
    _conf_file: str
    _val_conf_attr: list = []
    check_stage: int = 0
    @cached_property
    def read_conf(self):
        """
        Property to read the configuration file.
        Returns:
            ConfigParser: The parsed configuration object.
        """
        config = configparser.ConfigParser()
        config.read(self._conf_file)
        return config
    def __str__(self):
        """
        Returns the name of the Config class as a string.
        Returns:
            str: The name of the Config class.
        """
        name = self.__class__.__name__
        return name
    def __getattr__(self, val):
        """
        Retrieves the value of a configuration attribute.
        Args:
            val (str): The name of the configuration attribute.
        Returns:
            str: The value of the configuration attribute.
        """
        if self.check_stage == 0:
            self.check_stage = 1
            if val in self._val_conf_attr:
                self.check_stage = 0
                conf = self.read_conf[str(self)][val]
                # If the configuration value starts with '[' (indicating it's a list-like representation),
                # evaluate it using eval to convert it into an actual list object.
                if conf.startswith('['):
                    conf = conf[2:-2].split("\', \'")
                return conf
            self.check_stage = 0
        else:
            return self.__getattribute__(val)
class Page(ABC):
    """
    Abstract base class representing a web page.
    Attributes:
        xpaths (list): A list of XPath expressions to extract items from the page.
        next_xpaths (list): A list of XPath expressions to locate the next page link.
        _ix (int): Internal index for iteration.
    Methods:
        as_item: Abstract method to convert HTML content to an Item object.
        __init__: Initializes a Page object with the provided response.
        __len__: Returns the number of items on the page.
        __rshift__: Defines the behavior for the '>>' operator.
        __iter__: Returns an iterator object.
        __next__: Returns the next item in iteration.
        __getitem__: Retrieves the item at the specified index.
    """
    xpaths: list[str]
    next_xpaths: list[str]
    _ix: int = 0
    @abstractmethod
    def as_item(self, html) -> Item:
        """
        Abstract method to convert HTML content to an Item object.
        Args:
            html: HTML content of the page.
        Returns:
            Item: The parsed item from the HTML content.
        """
    def __init__(self, response):
        """
        Initializes a Page object with the provided response.
        Args:
            response: The response object from the web request.
        """
        self.response = response
        self.page_items = self.response.xpath('|'.join(self.xpaths))
        self.next = self.response.xpath('|'.join(self.next_xpaths)).get()
    def __len__(self):
        """
        Returns the number of items on the page.
        Returns:
            int: The number of items on the page.
        """
        return len(self.page_items)
    def __iter__(self):
        """
        Returns an iterator object.
        Returns:
            iterator: An iterator object.
        """
        return self
    def __next__(self):
        """
        Returns the next item in iteration.
        Returns:
            Item: The next item on the page.
        Raises:
            StopIteration: If all items have been iterated.
        """
        if self._ix < len(self):
            self._ix += 1
            return self[self._ix - 1]
        self._ix = 0
        raise StopIteration
    def __getitem__(self, ix):
        """
        Retrieves the item at the specified index.
        Args:
            ix (int): The index of the item to retrieve.
        Returns:
            Item: The item at the specified index.
        """
        return self.as_item(self.page_items[ix])
class Site:
    """
    A class representing a website.
    Attributes:
        name (str): The name of the website.
        start_urls (list): A list of starting URLs for the web crawler.
        Page (Page): The page parser class.
        db (str, optional): The database connection string. Defaults to None.
    Methods:
        spider: A property returning a spider class for scraping.
    """
    name: str
    start_urls: list
    pageclass: Page
    follow: bool = True
    class Db:
        """
        Default Db Class
        """
        @staticmethod
        def push(val):
            """
            No-change
            """
            return val
    @property
    def spider(self) -> SiteSpider:
        """
        Returns a spider class for scraping.
        Returns:
            class: A spider class for scraping data from the website.
        """
        class SiteSpider(Spider):
            """
            A spider class for scraping data from the website.
            Attributes:
                name (str): The name of the spider.
                start_urls (list): A list of starting URLs for scraping.
                Page (Page): The page parser class.
                engine (str): The engine used for parsing.
            """
            name = self.name
            start_urls = self.start_urls
            pageclass = self.pageclass
            db = self.Db
            follow = self.follow
            def parse(self, response):
                """
                Parses the response from the website.
                Args:
                    response: The response from the website.
                Yields:
                    dict: The scraped data items.
                """
                for item in (page := self.pageclass(response)):
                    item >> self.db
                    yield item.to_dict()
                if page.next and self.follow:
                    response.follow(page.next, callback=self.parse)
        return SiteSpider
