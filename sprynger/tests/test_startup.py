"""Test the startup of the sprynger package."""
import os
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

def test_init_with_env_variables():
    """Test initialization with environment variables."""
    # Save original env vars
    original_api_key = os.environ.get('API_KEY')
    original_api_key_meta = os.environ.get('API_KEY_META')
    original_api_key_oa = os.environ.get('API_KEY_OA')
    
    try:
        # Test API_KEY_META and API_KEY_OA env vars
        os.environ['API_KEY_META'] = 'env_meta_key'
        os.environ['API_KEY_OA'] = 'env_oa_key'
        init()
        assert get_key('Meta') == 'env_meta_key'
        assert get_key('OpenAccess') == 'env_oa_key'
        
        # Test that specific env vars override API_KEY
        os.environ['API_KEY'] = 'env_default_key'
        os.environ['API_KEY_META'] = 'env_meta_override'
        init()
        assert get_key('Meta') == 'env_meta_override'
        assert get_key('OpenAccess') == 'env_oa_key'
        
        # Test that explicit params override env vars
        init(api_key_meta='explicit_meta')
        assert get_key('Meta') == 'explicit_meta'
        
    finally:
        # Restore original env vars
        if original_api_key is not None:
            os.environ['API_KEY'] = original_api_key
        elif 'API_KEY' in os.environ:
            del os.environ['API_KEY']
            
        if original_api_key_meta is not None:
            os.environ['API_KEY_META'] = original_api_key_meta
        elif 'API_KEY_META' in os.environ:
            del os.environ['API_KEY_META']
            
        if original_api_key_oa is not None:
            os.environ['API_KEY_OA'] = original_api_key_oa
        elif 'API_KEY_OA' in os.environ:
            del os.environ['API_KEY_OA']
