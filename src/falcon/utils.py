from os import path
import re

from typing import Union


def dir(file):
    return path.join(
        path.dirname(path.realpath(__file__)),
        file
    )
phone=r'[\s\-]{0,1}?'.join([
                r'\+{0,1}?\d{0,3}',
                r'(\d{2}',
                r'\d{3}',
                r'\d{2}',
                r'\d{2})'
                ])
currency = r'(\d{1}.*?)[^\d\s,.]'
def ravel(value:Union[str,list[str],set[str]],sep=' ')->str:
    """
    This function takes a value as input, which can be a string, list of strings, or a set of strings.
    If the input is a set or list, the function concatenates the strings into a single string separated by spaces.
    Then, it removes newline characters and multiple spaces from the string.
    
    Parameters:
    value (Union[str,list[str],set(str)]): The input value to be raveled.
    
    Returns:
    str: The raveled string with removed newline characters and multiple spaces.
    """
    if isinstance(value,(set,list)):
        value = sep.join(set(value))
    raveled = value.replace('\n',' ')
    removed_multiple_spaces = re.sub(r'\s+',' ',raveled)
    return removed_multiple_spaces.strip()