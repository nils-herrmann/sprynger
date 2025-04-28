'''Constants for the sprynger package.'''
from pathlib import Path
from platformdirs import user_cache_dir

BASE_URL = 'http://api.springernature.com'

BASE_PATH = Path(user_cache_dir('sprynger'))
DEFAULT_PATHS = {
    'Metadata': BASE_PATH/'metadata',
    'Meta': BASE_PATH/'meta',
    'OpenAccess': BASE_PATH/'open_access'
}

ONLINE_API = {
    'Metadata': 'metadata',
    'Meta': '/meta/v2',
    'OpenAccess': 'openaccess'
}

FORMAT = {
    'Metadata': 'json',
    'Meta': 'json',
    'OpenAccess': 'jats'
}

LIMIT = {
    'Basic': {
        'Metadata': 25,
        'Meta': 25,
        'OpenAccess': 20,
        'OpenAccessJournal': 20,
        'OpenAccessBook': 20,
    },
    'Premium': {
        'Metadata': 25,
        'Meta': 25,
        'OpenAccess': 20,
        'OpenAccessJournal': 20,
        'OpenAccessBook': 20,
    },
}

REQUESTS = {
    'Timeout': 20,
    'Retries': 5,
    'BackoffFactor': 2.0
}

VALID_FIELDS = {
    "doi": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "subject": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "keyword": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "language": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "pub": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "year": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "onlinedate": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "onlinedatefrom": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "onlinedateto": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "datefrom": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "dateto": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "dateloaded": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "dateloadedfrom": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "dateloadedto": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "country": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "isbn": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "issn": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "journalid": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "topicalcollection": {
        "api": ["Metadata", "Meta"],
        "plan": ["Premium"]
    },
    "journalonlinefirst:true": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "date": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "issuetype": {
        "api": ["Metadata", "Meta"],
        "plan": ["Premium"]
    },
    "issue": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "volume": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "type": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Basic", "Premium"]
    },
    "ContainsElements": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "excludeElements": {
        "api": ["OpenAccess"],
        "plan": ["Premium"]
    },
    "Exclude:Bibliography": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "grid": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "orcid": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "bookdoi": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "latest issue": {
        "api": ["Metadata", "Meta"],
        "plan": ["Premium"]
    },
    "earliest issue": {
        "api": ["Metadata", "Meta"],
        "plan": ["Premium"]
    },
    "openaccess:true": {
        "api": ["Meta"],
        "plan": ["Premium"]
    },
    "free:true": {
        "api": ["Meta"],
        "plan": ["Premium"]
    },
    "title:": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "orgname:": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "journal:": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "book:": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "name:": {
        "api": ["Metadata", "OpenAccess", "Meta"],
        "plan": ["Premium"]
    },
    "sort:date": {
        "api": ["Metadata", "Meta"],
        "plan": ["Premium"]
    },
    "sort:sequence": {
        "api": ["Metadata", "Meta"],
        "plan": ["Premium"]
    }
}


INCLUDED_TAGS = {
    # Main body text elements
    'p', 'sec', 'title', 'subtitle', 'disp-quote', 'list', 'list-item', 'def-list', 'def-item',
    # Inline formatting
    'italic', 'bold', 'underline', 'monospace', 'sup', 'sub', 'sc', 'break',
    # Special blocks
    #'fig', 'caption', 'table-wrap', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'code', 'preformat',
    # References and links
    'xref', 'ext-link', 'uri',
    # Math
    #'inline-formula', 'disp-formula',
    # Misc
    'label'
}
