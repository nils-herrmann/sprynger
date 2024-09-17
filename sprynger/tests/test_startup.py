"""Test the startup of the sprynger package."""
from pathlib import Path

from sprynger import init
from sprynger.utils.startup import CUSTOM_KEYS, get_config, get_keys
from sprynger import OpenAccessBook


def test_empty_keys():
    """Test the empty keys."""
    assert CUSTOM_KEYS is None


def test_file_not_found():
    """Test the FileNotFoundError."""
    try:
        _ = OpenAccessBook("10.1007/978-3-031-61874-1_5", refresh=30)
    except FileNotFoundError:
        assert True


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
