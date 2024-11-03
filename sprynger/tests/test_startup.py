"""Test the startup of the sprynger package."""
from sprynger import init
from sprynger.utils.parse import chained_get
from sprynger.utils.startup import get_config, get_key

def test_custom_api():
    """Test use of custom config file"""
    init(api_key='not existing key',
         config_file='./sprynger/tests/test_config.toml')
    config = get_config()
    assert chained_get(config, ['Directories', 'Metadata']) == './sprynger/tests/'

def test_init():
    """Test the init function."""
    init()
    assert get_config() is not None
    assert get_key() is not None
