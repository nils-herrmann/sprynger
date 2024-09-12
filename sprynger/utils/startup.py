from configparser import ConfigParser

from sprynger.utils.constants import CONFIG_FILE


def get_config():
    """Get configuration settings from the configuration file."""
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config

