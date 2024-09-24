"""Test the startup of the sprynger package."""
from pathlib import Path

from sprynger import init
from sprynger.utils.startup import CUSTOM_KEYS, get_config, get_keys


def test_empty_keys():
    """Test the empty keys."""
    assert CUSTOM_KEYS is None


def test_init():
    """Test the init function."""
    init()
    assert get_config() is not None
    assert get_keys() is not None


def test_create_config():
    """Test the create_config function."""
    config_dir = Path.home()/'.config'/'sprynger'/'test_sprynger.cfg'
    # Dete file
    config_dir.unlink(missing_ok=True)
    assert not config_dir.exists()
    # Create file
    init(config_dir, ['test_key'])
    assert config_dir.exists()
