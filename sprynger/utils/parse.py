"""Utility functions for parsing data."""
from functools import reduce
from typing import Optional

from lxml.etree import _Element


def get_attr(node: _Element,
             tag: str,
             attr: str,
             value: str) -> Optional[str]:
    """Get the attribute of a tag in an XML node."""
    if node.find(f'.//{tag}[@{attr}="{value}"]') is not None:
        return node.find(f'.//{tag}[@{attr}="{value}"]').text
    return None


def get_text(node: _Element,
             path: str) -> Optional[str]:
    """Get the text of an XML node."""
    if node.find(path) is not None:
        return node.find(path).text
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