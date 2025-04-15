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

API_KEY = None
CONFIG = None


def init(api_key: Optional[str] = None,
         config_file: Optional[Union[str, Path]] = None) -> None:
    """
    Function to initialize the sprynger library. For more information go to the
    `documentation <file:///Users/nilsherrmann/sprynger/docs/build/html/initialization.html#configuration>`_.
    
    Args:
        api_key (str): API key
        config_file (str): Path to the configuration .toml file.
        
    
    Raises:
        ValueError: If no api key was provided either as argument or as an
        environment variable `API_KEY`.
    
    Example:
        >>> from sprynger import init
        >>> init(key='your key', config_file='path/to/custom/config.toml')
    """
    global API_KEY
    global CONFIG

    CONFIG = _load_default_config()

    if config_file:
        with open(config_file, 'rb') as f:
            custom_config = tomllib.load(f)
        _merge_dicts(CONFIG, custom_config)

    _create_cache_folders(CONFIG)

    API_KEY = api_key or os.environ.get("API_KEY")
    if not API_KEY:
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


def get_key() -> str:
    """Function to get the API keys and overwrite keys in config if needed."""
    return API_KEY
