"""
Module Test Instances

This module contains test functions for the creation of instances of different classes in the Model module.

Functions:
- test_formatter_instance(): Tests the creation of a Formatter class instance.
- test_field_instance(): Tests the creation of a Field class instance.
- test_item_instance(): Tests the creation of an Item class instance.
- test_page_instance(): Tests the creation of a Page class instance.
- test_MainItem_instance(): Tests the creation of a MainItem class instance.
"""
from vacuum import Model
from vacuum import Item
from scrapy import Selector
from dataclasses import dataclass

import pytest

def test_formatter_instance():
    """
    Test for the creation of a Formatter class instance. It checks if a TypeError is raised when trying to create an instance.
    """
    with pytest.raises(TypeError):
        Model.Formatter()
    print("TypeError Raised")

def test_field_instance():
    """
    Test for the creation of a Field class instance. It checks if a TypeError is raised when trying to create an instance.
    """
    with pytest.raises(TypeError):
        Model.Field()
    print("TypeError Raised")

def test_item_instance():
    """
    Test for the creation of an Item class instance. It checks if the created instance is an instance of the Item class.
    """
    item = Model.Item()
    isinstance(item, Model.Item)

def test_page_instance():
    """
    Test for the creation of a Page class instance. It checks if a TypeError is raised when trying to create an instance.
    """
    with pytest.raises(TypeError):
        Model.Page()
    print("TypeError Raised")

def test_MainItem_instance():
    """
    Test for the creation of a MainItem class instance. It parses HTML text into a MainItem object.
    It asserts that the parsed object's class name is 'MainItem'.
    """
    html = '''<div></div>'''
    mi = Item.MainItem.parse(Selector(text=html))
    assert mi.__class__.__name__ == 'MainItem'