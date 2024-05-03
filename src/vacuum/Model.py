"""
This module implements a development model with the following classes:

- Formatter: A helper class for string formatting.

- Field: An abstract class for creating Fields.

- Item: A class for instances with fields.

The Formatter class provides methods to format strings using placeholders and values.

The Field class is an abstract base class that can be inherited to create custom fields for items.

The Item class represents an instance with multiple fields, which can be accessed and manipulated using the Field objects.

Usage:

    ```python
        >>> from .model import Formatter, Field, Item
        >>> formatter = Formatter()
        >>> field = Field()
        >>> item = Item()
    ```

Imports:

    - annotations : Importing 'from future import annotations' enables the use of postponed evaluation of annotations in type hints, allowing the use of class names before their definition.

    - ABC, abstractmethod : The 'ABC' and 'abstractmethod' imports from 'abc' module provide tools for creating abstract base classes and abstract methods.

    - wraps,_Wrapped : The 'wraps' and '_Wrapped' imports from 'functools' module are used for creating decorator functions that preserve the metadata of the original function.

    - dateparser : The 'dateparser' import provides functionality for parsing date and time strings into human-readable format.

    - logging : The 'logging' import allows for creating log messages, setting log level, and configuring logging behavior in the application.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from functools import wraps,cached_property
import dateparser
import logging
logger = logging.getLogger()
from dataclasses import field as dcl_field,asdict, dataclass, make_dataclass
from datetime import datetime
import configparser
class Formatter(ABC):
    """
    This class 'Formatter' provides methods for string formatting and casting values.

    Methods:

        cast(func): A static method that wraps a function to capture any exceptions and log warnings if the function fails.
        fmethod property: A property that allows getting and setting the formatting method for the Formatter.
        format(value): A method that applies the specified formatting method to the given value.

    Usage:
    ```python
        >>> formatter = Formatter
        >>> formatter.fmethod = custom_format_method
        >>> formatted_value = formatter.format(input_value)
    ```    
    """
    @staticmethod
    def cast(func) -> callable:
        """
        This method 'cast' is a static method within the Formatter class that wraps a function to handle parsing errors and log warnings if the function fails.

        Parameters:

            func: The function to be wrapped for error handling.
            value(str): The value to be passed to the wrapped function.

        Returns:

            wrapper: A wrapped function that captures and logs any exceptions that occur during the execution of the original function.
            
        Notes:
            The 'wrapper' function captures any exceptions raised by 'func' when called with 'value'. If an exception occurs, a warning message is logged using the 'logger' module. The method then returns the result of the 'func' call or None if an exception was caught.

            Note: This method is meant to be used as a decorator for methods that require error handling and logging for parsing or formatting operations.
        """
        @wraps(func)
        def wrapper(self,value:str):
            res = None
            try:
                res = func(self,value)
            except:
                logger.warning('failed parsing %s'%value)
            return res
        return wrapper
    @abstractmethod
    def fmethod(self,value):
        ...
    @cast
    def Format(self,value):
        return self.fmethod(value)
class Field(Formatter):
    """
    This class 'Field' extends the 'Formatter' class and represents a field with defined XPath expressions and regex patterns to extract values from HTML content.

    Attributes:
    - xpaths: A list of XPath expressions used to extract values from HTML content.
    - regex_list: A list of regex patterns used to further process extracted values.

    Methods:
    - get_value(): Extracts values from HTML content using the defined XPath expressions and returns the formatted result.

    Usage:
    - Create instances of the Field class with specified XPath expressions and regex patterns.
    - Call the 'get_value' method to extract values from HTML content using the defined XPath expressions and regex patterns.

    Note:
    - The Field class inherits from the 'Formatter' class and adds functionality for extracting values from HTML content.
    - The class encapsulates logic for extracting and formatting values from HTML content using XPath expressions and regex patterns.
    - The get_value method combines XPath extraction and regex processing to retrieve and format values from the HTML content.
    """
    xpaths:list[str]
    relative_xpaths:list[str]
    regex_list:list[str]
    def __init__(self,html):
        self.html = html
    def getter(self,paths='xpaths'):
        out = self.html.xpath('|'.join(self.__getattr__(paths))).getall()
        return self.Format(out)
    @cached_property      
    def value(self):
        return self.getter(paths='xpaths')
    @cached_property 
    def relative_value(self):
        return self.getter(paths='relative_xpaths')
class Item:
    
    """
    This class 'Item' represents an item with attributes defined dynamically using dataclasses.

    Attributes:
    - registry: A set that holds registered attribute fields for the Item class.
    - incs: A list of additional fields to include in the Item class.

    Methods:
    - register(FieldClass): Registers a new attribute field for the Item class.
    - __init__(): Constructs the Item class with dynamically created attributes based on the registered fields and additional fields.

    Usage:
    - Create instances of the Item class and register attribute fields using the 'register' method.
    - Define additional fields to include in the class using the 'incs' attribute.
    - Instantiate the Item class to create an object with dynamically generated attributes based on the registered fields and additional fields.

    Note:
    - The Item class uses dataclasses to dynamically create attribute fields based on the registered fields and the specified additional fields.
    - The register method allows for adding new attribute fields to the Item class at runtime.
    - The __init__ method constructs the Item class with the registered fields, additional fields, and a '__post_init__' method for post-initialization logic.
    """
    @classmethod
    def register(cls,FieldClass)->None:
        if not hasattr(cls,'registry'):
            cls.registry:set=set() 
        cls.registry.add(FieldClass)
    def __str__(self):
        return self.__class__.__name__
    @classmethod
    def parse(cls,html,method='value'):
        self = cls()
        item_fields = [
            (field.__name__,
             field.fmethod.__annotations__.get('return',str).__name__,
             getattr(field(html),method)) 
            for field in self.registry
            ]+ [('CreatedAt',datetime,datetime.now().isoformat())]
        return make_dataclass(str(self), item_fields)()
class Config:
    _conf_file :str
    _val_conf_attr:list=[]
    check_stage:int=0
    @cached_property
    def read_conf(self):
        config = configparser.ConfigParser()
        config.read(self._conf_file)
        return config
    def __str__(self):
        return self.__class__.__name__
    def __getattr__(self,val):
        if self.check_stage == 0:
            self.check_stage = 1
            if val in self._val_conf_attr:
                self.check_stage = 0
                conf = self.read_conf[str(self)][val]
                if conf.startswith('['):
                    conf = eval(conf)
                return conf
            self.check_stage = 0
        else :
            return self.__getattribute__(val)
class Page(ABC):
    """
    This abstract class 'Page' represents a webpage and provides methods for handling page content as items.

    Attributes:

        xpaths: A list of XPath expressions used to extract items from the page content.
        _ix: An internal counter used for iteration over page items.

    Methods:

        as_item(html): An abstract method that converts HTML content into an 'Item' object.
        init(response): Initializes the Page object with items extracted based on defined XPath expressions.
        len(): Returns the number of items in the page.
        iter(): Returns an iterator object for iterating over the page items.
        next(): Returns the next item in the iteration or raises StopIteration if there are no more items.
        getitem(ix): Returns the item at the specified index in the page items.

    Usage:

        Define a subclass of Page and implement the 'as_item' method to convert HTML content into an 'Item' object.
        Instantiate the subclass with a response object containing the HTML content.
        Use len(), iteration, and indexing to access and process items on the page. 
    """
    xpaths:list[str]
    next_xpaths:list[str]
    _ix:int=0
    @abstractmethod
    def as_item(self,html)->Item:
        ...
    def __init__(self,response):
        self.response = response
        self.page_items = self.response.xpath('|'.join(self.xpaths))
        self.next = self.response.xpath('|'.join(self.next_xpaths)).get()
    def __len__(self):
        return len(self.page_items)
    def __rshift__(self,f):
        ...
    def __iter__(self):
        return self 
    def __next__(self):
        if self._ix < len(self):
            self._ix += 1
            return self[self._ix-1]
        self._ix = 0
        raise StopIteration
    def __getitem__(self,ix):
        return self.as_item(self.page_items[ix])