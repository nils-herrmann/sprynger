"""Utility functions for parsing data."""
from functools import reduce
from typing import Optional, Union

from lxml.etree import _Element


def get_attr(node: Optional[_Element],
             tag: str,
             attr: str,
             value: str) -> Optional[str]:
    """Get the attribute of a tag in an XML node."""
    if node is not None:
        if node.find(f'.//{tag}[@{attr}="{value}"]') is not None:
            return node.find(f'.//{tag}[@{attr}="{value}"]').text
    return None

def chained_get(data: dict, keys: list, default=None) -> Union[str, int, float]:
    """
    Retrieve a value from a nested dictionary using a list of keys.

    Args:
        data (dict): The dictionary to search.
        keys (list): A list of keys representing the path to the value.

    Returns:
        The value at the specified path, or `default` if the path does not exist.
    """
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        else:
            return default
    return data


def get_text(node: Optional[_Element],
             path: str) -> Optional[str]:
    """Get the text of an XML node."""
    if node is not None:
        if node.find(path) is not None:
            return node.find(path).text
    return None


def stringify_descendants(node: Optional[_Element]) -> Optional[str]:
    """
    Filters and removes possible Nones in texts and tails.
    If descendants are present, it will return their text.
    ref: http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    """
    if node is not None:
        return "".join(node.itertext())
    return None


def make_int_if_possible(val):
    """Attempt a conversion to int type."""
    try:
        return int(val)
    except (TypeError, ValueError):
        return val


def str_to_bool(val):
    """Convert a string to a boolean."""
    if val.lower() in ['true', 't', 'yes', 'y', '1']:
        return True
    elif val.lower() in ['false', 'f', 'no', 'n', '0']:
        return False
    else:
        return val