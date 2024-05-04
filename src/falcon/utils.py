"""
Module containing utility functions for the project.
Functions:
    dir: Returns the path to a file in the current directory.
    ravel: Flattens and formats a string, list, or set.
"""
from os import path
import re
from typing import Union
def flatten_dict(d, parent_key='', sep=':'):
    """
    Flatten a dictionary with nested dictionaries and lists.

    Args:
        d (dict): The input dictionary to flatten.
        parent_key (str, optional): The parent key for recursion. Defaults to ''.
        sep (str, optional): The separator to use between keys. Defaults to '_'.

    Returns:
        dict: The flattened dictionary.
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, val in enumerate(v):
                if isinstance(val, dict) or isinstance(val, list):
                    items.extend(flatten_dict({str(i): val}, new_key, sep=sep).items())
                else:
                    items.append((f"{new_key}{sep}{i}", val))
        else:
            items.append((new_key, v))
    return dict(items)


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
