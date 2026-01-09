"""Module to initialize the sprynger library."""
try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib 

import os

from pathlib import Path
from typing import Optional, Union

from sprynger.exceptions import MissingAPIKeyError
from sprynger.utils.constants import DEFAULT_PATHS, REQUESTS

API_KEYS = None
CONFIG = None


def init(api_key: Optional[str] = None,
         api_key_meta: Optional[str] = None,
         api_key_oa: Optional[str] = None,
         config_file: Optional[Union[str, Path]] = None) -> None:
    """
    Function to initialize the sprynger library. For more information go to the
    `documentation <file:///Users/nilsherrmann/sprynger/docs/build/html/initialization.html#configuration>`_.
    
    Args:
        api_key (str): API key (for backward compatibility, will be used for both Meta and OpenAccess)
        api_key_meta (str): API key for Meta API
        api_key_oa (str): API key for OpenAccess API
        config_file (str): Path to the configuration .toml file.
        
    
    Raises:
        ValueError: If no api key was provided either as argument or as an
        environment variable `API_KEY`.
    
    Example:
        >>> from sprynger import init
        >>> init(api_key='your key')
        >>> init(api_key_meta='meta_key', api_key_oa='oa_key')
        >>> init(api_key='your key', api_key_meta='meta_key', api_key_oa='oa_key')
    """
    global API_KEYS
    global CONFIG

    CONFIG = _load_default_config()

    if config_file:
        with open(config_file, 'rb') as f:
            custom_config = tomllib.load(f)
        _merge_dicts(CONFIG, custom_config)

    _create_cache_folders(CONFIG)

    # Get api_key from environment if not provided
    env_api_key = os.environ.get("API_KEY")
    
    # If api_key is provided or available in env, use it as default for both
    default_key = api_key or env_api_key
    
    # Set API keys with fallback to default_key
    meta_key = api_key_meta or default_key
    oa_key = api_key_oa or default_key
    
    # Store keys in a dictionary
    API_KEYS = {
        'Meta': meta_key,
        'Metadata': meta_key,  # Metadata uses the same key as Meta
        'OpenAccess': oa_key
    }
    
    # Check that at least one key is provided
    if not any(API_KEYS.values()):
        raise ValueError('No API key found. Provide an API key or set the '
                         'environment variable API_KEY. To get an API key '
                         'visit: https://dev.springernature.com/')


def _load_default_config() -> dict:
    """Auxiliary function to load the default configuration."""
    config = {}
    config['Directories'] = DEFAULT_PATHS
    config['Requests'] = REQUESTS
    return config


def _merge_dicts(default, custom):
    """
    Recursively merge two dictionaries. The values from the custom dictionary
    will overwrite those from the default dictionary.
    """
    for key, value in custom.items():
        if isinstance(value, dict) and key in default:
            _merge_dicts(default[key], value)
        else:
            default[key] = value

def _create_cache_folders(config: dict) -> None:
    """Auxiliary function to create cache folders."""
    directories = config.get('Directories', {})
    for _, path in directories.items():
        cache_path = Path(path)
        cache_path.mkdir(parents=True, exist_ok=True)


def get_config() -> dict:
    """Function to get the config parser."""
    if not CONFIG:
        raise MissingAPIKeyError('Library not initialized. '
                                'Please initialize sprynger with init().\n'
                                'For more information visit: '
                                'the documentation.')
    return CONFIG


def get_key(api: str = 'Meta') -> str:
    """Function to get the API key for the specified API.
    
    Args:
        api (str): The API type ('Meta', 'Metadata', or 'OpenAccess'). Defaults to 'Meta'.
        
    Returns:
        str: The API key for the specified API.
        
    Raises:
        MissingAPIKeyError: If the library is not initialized or if no key exists for the specified API.
        ValueError: If an invalid API type is provided.
    """
    if not API_KEYS:
        raise MissingAPIKeyError('Library not initialized. '
                                'Please initialize sprynger with init().\n'
                                'For more information visit: '
                                'the documentation.')
    
    # Validate API type
    if api not in API_KEYS:
        raise ValueError(f'Invalid API type: {api}. '
                        f'Valid types are: {", ".join(API_KEYS.keys())}')
    
    key = API_KEYS.get(api)
    if not key:
        raise MissingAPIKeyError(f'No API key found for {api} API. '
                                f'Please initialize with appropriate key. '
                                f'Use api_key_meta for Meta/Metadata APIs, '
                                f'or api_key_oa for OpenAccess API.')
    return key
