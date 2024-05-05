"""
Module for managing CSS fields and related functionalities.
Classes:
    CssField: A class representing a CSS field.
    ProductTitle: A class representing the title of a product.
    VendorLocation: A class representing the location of a vendor.
    PublishDate: A class representing the publish date of an item.
    Contact: A class representing contact information.
    PublishLink: A class representing the publish link of an item.
    ProductPrice: A class representing the price of a product.
"""
import dateparser
from .Model import Field,ParseError
from .Item import MainItem
from .Css import MainCss
from .utils import phone, currency, ravel, re
class CssField(Field, MainCss):
    """
    A class representing a CSS field.
    Attributes:
        css (list): A list of CSS attributes.
    Methods:
        fmethod: Method defining the behavior for formatting CSS values.
    """
    css = [
        'xpaths',
        'relative_xpaths']
    def fmethod(self, value: str) -> str:
        """
        Formats the given CSS value.
        Args:
            value (str): The CSS value to format.
        Returns:
            str: The formatted CSS value.
        """
        return ravel(value)
@MainItem.register
class ProductTitle(CssField):
    """
    A class representing the title of a product.
    Inherits:
        CssField
    Methods:
        fmethod: Method defining the behavior for formatting product titles.
    """
    ...
@MainItem.register
class VendorLocation(CssField):
    """
    A class representing the location of a vendor.
    Inherits:
        CssField
    """
    ...
@MainItem.register
class PublishDate(CssField):
    """
    A class representing the publish date of an item.
    Inherits:
        CssField
    Methods:
        fmethod: Method defining the behavior for formatting publish dates.
    """
    def fmethod(self, value: str) -> str:
        """
        Formats the given publish date value.
        Args:
            value (str): The publish date value to format.
        Returns:
            str: The formatted publish date value.
        """
        date = dateparser.parse(ravel(value))
        if date:
            return date.isoformat()
        else :
            raise ParseError
@MainItem.register
class Contact(CssField):
    """
    A class representing contact information.
    Inherits:
        CssField
    Methods:
        fmethod: Method defining the behavior for formatting contact information.
    """
    def fmethod(self, value: str) -> str:
        """
        Formats the given contact information.
        Args:
            value (str): The contact information to format.
        Returns:
            str: The formatted contact information.
        """
        return re.sub(r'[\s\-\+]','',';'.join(set(re.findall(phone,ravel(value)))))
@MainItem.register
class PublishLink(CssField):
    """
    A class representing the publish link of an item.
    Inherits:
        CssField
    Methods:
        fmethod: Method defining the behavior for formatting publish links.
    """
    def fmethod(self, value: str) -> str:
        """
        Formats the given publish link value.
        Args:
            value (str): The publish link value to format.
        Returns:
            str: The formatted publish link value.
        """
        return ravel(value,sep=';')
@MainItem.register
class ProductPrice(CssField):
    """
    A class representing the price of a product.
    Inherits:
        CssField
    Methods:
        fmethod: Method defining the behavior for formatting product prices.
    """
    def fmethod(self, value: str) -> str:
        """
        Formats the given product price value.
        Args:
            value (str): The product price value to format.
        Returns:
            str: The formatted product price value.
        """
        return re.sub(r'[\s,\.]','',';'.join(re.findall(currency,ravel(value,sep=';'))))
