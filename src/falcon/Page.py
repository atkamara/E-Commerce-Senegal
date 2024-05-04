"""
Module for defining the MainPage class.
Classes:
    MainPage: A class representing a main page, inheriting from Page and MainCss.
Attributes:
    css (list): A list of CSS attributes.
"""
from .Model import Page
from .Item import MainItem
from .Css import MainCss
class MainPage(Page, MainCss):
    """
    A class representing a main page, inheriting from Page and MainCss.    Attributes:
        css (list): A list of CSS attributes.
    Methods:
        as_item: Converts HTML content to a MainItem object.
    """
    css = [
        'xpaths',
        'next_xpaths']
    def as_item(self, html):
        """
        Converts HTML content to a MainItem object.
        Args:
            html: The HTML content to parse.
        Returns:
            MainItem: The parsed MainItem object.
        """
        return MainItem.parse(html, method='relative_value')
