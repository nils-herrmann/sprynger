"""Module to test the Retrieve class."""
import pytest

from sprynger import init
from sprynger.retrieve import Retrieve

init()

def test_check_query():
    """Test the _check_query method."""
    with pytest.raises(ValueError, match="Please provide a query or kwargs."):
        Retrieve('', 'OpenAccess')

    error_str = f"Invalid field: erroneus_field."
    with pytest.raises(ValueError, match=error_str):
        Retrieve('', api='Meta', erroneus_field='Neural Network')

    error_str = f"Field topicalcollection is not available in OpenAccess."
    with pytest.raises(ValueError, match=error_str):
        Retrieve('', api='OpenAccess', topicalcollection='Neural Network')

    error_str = f"Field topicalcollection is not available in Basic plan."
    with pytest.raises(ValueError, match=error_str):
        Retrieve('', api='Meta', premium=False, topicalcollection='Neural Network')
