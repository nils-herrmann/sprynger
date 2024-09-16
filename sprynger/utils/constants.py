"""Constants for the sprynger package."""
from pathlib import Path

BASE_URL = 'http://api.springernature.com'

CONFIG_FILE = Path.home()/'.config'/'sprynger'/'sprynger.cfg'

BASE_PATH = Path.home()/'.cache'/'sprynger'
DEFAULT_PATHS = {
    'Metadata': BASE_PATH/'metadata',
    'Meta': BASE_PATH/'meta',
    'OpenAccess': BASE_PATH/'open_access',
}

FORMAT = {
    'Metadata': 'json',
    'Meta': 'json',
    'OpenAccess': 'jats'
}
