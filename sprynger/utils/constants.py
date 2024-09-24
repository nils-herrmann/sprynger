'''Constants for the sprynger package.'''
from pathlib import Path

BASE_URL = 'http://api.springernature.com'

CONFIG_FILE = Path.home()/'.config'/'sprynger'/'sprynger.cfg'

BASE_PATH = Path.home()/'.cache'/'sprynger'
DEFAULT_PATHS = {
    'Metadata': BASE_PATH/'metadata',
    'Meta': BASE_PATH/'meta',
    'OpenAccessJournal': BASE_PATH/'open_access'/'journal',
    'OpenAccessBook': BASE_PATH/'open_access'/'book',
}

ONLINE_API = {
    'Metadata': 'metadata',
    'Meta': '/meta/v2',
    'OpenAccessJournal': 'openaccess',
    'OpenAccessBook': 'openaccess'
}

FORMAT = {
    'Metadata': 'json',
    'Meta': 'json',
    'OpenAccessJournal': 'jats',
    'OpenAccessBook': 'jats'
}

LIMIT = {
    'Basic': {
        'Metadata': 25,
        'Meta': 25,
        'OpenAccessJournal': 20,
        'OpenAccessBook': 20,
    },
    'Premium': {
        'Metadata': 25,
        'Meta': 25,
        'OpenAccessJournal': 20,
        'OpenAccessBook': 20,
    },
}
