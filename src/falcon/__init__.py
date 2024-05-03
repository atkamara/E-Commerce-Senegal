"""
falcon package

This package contains modules related to data formatting and structured representation.

Modules:
- Fields.py
- Item.py
- Model.py
- Page.py

To use the package, import the specific modules as needed. For example:
    from falcon.Fields import Field
    from falcon.Item import Item
    from falcon.Model import Model
    from falcon.Page import Page
"""
from __future__ import annotations
from . import Fields #must be imported in priority before item
from . import Item
from . import Model
from . import Page

__version__ = "0.0.1"
__author__ = 'atkamara'