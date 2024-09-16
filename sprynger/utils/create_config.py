"""This module contains the function to create a configuration file."""
import configparser
from pathlib import Path
from typing import Optional

from sprynger.utils.constants import CONFIG_FILE


def create_config(config_dir: Optional[Path] = None,
                  keys: Optional[list[str]] = None
                  ):
    """Initiates process to generate configuration file.

    :param keys: If you provide a list of keys, sprynger will skip the prompt.
    """
    from sprynger.utils.constants import DEFAULT_PATHS

    if not config_dir:
        config_dir = CONFIG_FILE

    config = configparser.ConfigParser()
    config.optionxform = str
    print(f"Creating config file at {config_dir} with default paths...")

    # Set directories
    config.add_section('Directories')
    for api, path in DEFAULT_PATHS.items():
        config.set('Directories', api, str(path))

    # Set authentication
    config.add_section('Authentication')
    if keys:
        if not isinstance(keys, list):
            raise ValueError("Parameter `keys` must be a list.")
        key = ", ".join(keys)
    else:
        prompt_key = "Please enter your API Key(s), obtained from "\
                     "https://dev.springernature.com.  Separate "\
                     "multiple keys by comma:\n"
        key = input(prompt_key)
    config.set('Authentication', 'APIKey', key)

    # Set default values
    config.add_section('Requests')
    config.set('Requests', 'Timeout', '20')
    config.set('Requests', 'Retries', '5')

    # Write out
    config_dir.parent.mkdir(parents=True, exist_ok=True)
    with open(config_dir, "w") as ouf:
        config.write(ouf)
    print(f"Configuration file successfully created at {config_dir}\n"
          "For details see https://sprynger.rtfd.io/en/stable/initialization.html.")
    return config
