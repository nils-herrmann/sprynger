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
    assert get_key('Meta') is not None
    assert get_key('OpenAccess') is not None

def test_init_with_separate_keys():
    """Test initialization with separate keys for Meta and OpenAccess."""
    init(api_key_meta='meta_key_test', api_key_oa='oa_key_test')
    assert get_key('Meta') == 'meta_key_test'
    assert get_key('OpenAccess') == 'oa_key_test'
    assert get_key('Metadata') == 'meta_key_test'  # Metadata uses same key as Meta

def test_init_with_single_key():
    """Test backward compatibility with single api_key."""
    init(api_key='single_key_test')
    assert get_key('Meta') == 'single_key_test'
    assert get_key('OpenAccess') == 'single_key_test'
    assert get_key('Metadata') == 'single_key_test'

def test_init_with_mixed_keys():
    """Test initialization with both api_key and specific keys."""
    init(api_key='default_key', api_key_meta='meta_specific', api_key_oa='oa_specific')
    assert get_key('Meta') == 'meta_specific'
    assert get_key('OpenAccess') == 'oa_specific'
    # Specific keys should override the general api_key
