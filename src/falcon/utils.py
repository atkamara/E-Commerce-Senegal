"""
Module containing utility functions for the project.

Functions:
    dir: Returns the path to a file in the current directory.
    ravel: Flattens and formats a string, list, or set.
"""

from os import path
import re

from typing import Union

def dir(file: str) -> str:
    """
    Returns the path to a file in the current directory.

    Args:
        file (str): The name of the file.

    Returns:
        str: The full path to the file.
    """
    return path.join(
        path.dirname(path.realpath(__file__)),
        file
    )

phone = r'[\s\-]{0,1}?'.join([
    r'\+{0,1}?\d{0,3}',
    r'(\d{2}',
    r'\d{3}',
    r'\d{2}',
    r'\d{2})'
])

currency = r'(\d{1}.*?)[^\d\s,.]'

def ravel(value: Union[str, list[str], set[str]], sep: str = ' ') -> str:
    """
    Flattens and formats a string, list, or set.

    Args:
        value (Union[str, list[str], set[str]]): The value to flatten and format.
        sep (str, optional): The separator to use when joining elements. Defaults to ' '.

    Returns:
        str: The flattened and formatted value.
    """
    if isinstance(value, (set, list)):
        value = sep.join(set(value))
    raveled = value.replace('\n', ' ')
    removed_multiple_spaces = re.sub(r'\s+', ' ', raveled)
    return removed_multiple_spaces.strip()
