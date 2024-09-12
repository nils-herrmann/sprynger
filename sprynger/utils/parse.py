from functools import reduce

def chained_get(container, path, default=None):
    """Helper function to perform a series of .get() methods on a dictionary
    or return the `default`.

    Parameters
    ----------
    container : dict
        The dictionary on which the .get() methods should be performed.

    path : list or tuple
        The list of keys that should be searched for.

    default : any (optional, default=None)
        The object type that should be returned if the search yields
        no result.
    """
    # Obtain value via reduce
    try:
        return reduce(lambda c, k: c.get(k, default), path, container)
    except (AttributeError, TypeError):
        return default


def listify(element):
    """Helper function to turn an element into a list if it isn't a list yet.
    """
    if isinstance(element, list):
        return element
    else:
        return [element]


def make_float_if_possible(val):
    """Attempt a conversion to float type."""
    try:
        return float(val)
    except TypeError:
        return val


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