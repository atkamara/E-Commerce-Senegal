"""
Module for managing CSS configurations.
Classes:
    MainCss: A class for managing main CSS configurations.
"""
from .Model import Config
from functools import cached_property
from .utils import dir
class MainCss(Config):
    """
    A class for managing main CSS configurations.
    Attributes:
        _conf_file (str): The path to the CSS configuration file.
    
    Methods:
        _val_conf_attr: Property returning the valid CSS attributes.
    """
    _conf_file: str = dir('css.ini')
    @cached_property
    def _val_conf_attr(self) -> list:
        """
        Property returning the valid CSS attributes.
        Returns:
            list: A list of valid CSS attributes.
        """
        return self.css
