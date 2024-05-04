"""
Initialization module for the falcon project.
Imports:
    Fields: Module containing field definitions.
    Item: Module containing item definitions.
    Model: Module containing model definitions.
    Page: Module containing page definitions.
Attributes:
    __version__ (str): The version number of the project.
    __author__ (str): The author of the project.
"""
from __future__ import annotations
from . import Fields  # Must be imported in priority before item
from . import Item
from . import Model
from . import Page
__version__ = "0.0.1"
__author__ = 'atkamara'
