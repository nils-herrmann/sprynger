Start-up
========

You initalize `sprynger` as follows:

.. code:: python

    >>> import sprynger

    >>> sprynger.init()

This reads the configuration from the default locations. You may also specify a different configuration file and API keys:

.. function:: init(config_dir: Union[str, Path], keys: Optional[List[str]])

   Function to initialize the sprynger library. For more information, see the 
   `documentation <file:///Users/nilsherrmann/sprynger/docs/build/html/initialization.html#configuration>`_.

   :param config_dir: Path to the configuration file (default is `~/.config/sprynger/sprynger.cfg`).
   :type config_dir: str
   :param keys: List of API keys (default is None).
   :type keys: list, optional

   :raises FileNotFoundError: If the configuration file is not found.

   **Example**:

   .. code:: python

      >>> from sprynger import init
      >>> init(config_dir='path/to/custom/config.cfg', keys=['key1', 'key2'])


In case you don't have a configuration file just enter your API key when prompted.


Configuration
=============

`sprynger` stores values it needs for operation in a configuration file called `sprynger.cfg`. 
The config file saves credentials as well as directory names for folders that store downloaded results.
`sprynger` reads this file on startup.

You can find the configuration file in: `~/.config/sprynger/sprynger.cfg`

By default, after initial set-up (see below), the file will look like this:

.. code-block:: cfg

    [Directories]
    Metadata = /Users/user/.cache/sprynger/metadata
    Meta = /Users/user/.cache/sprynger/meta
    OpenAccess = /Users/user/.cache/sprynger/open_access

    [Authentication]
    APIKey = XXX

    [Requests]
    Timeout = 20
    Retries = 5
    BackoffFactor = 2.0


Section `[Directories]` contains the paths where `sprynger` should store (cache) downloaded files.  `sprynger` will create them if necessary.

Section `[Authentication]` contains the API Keys which you obtain from https://dev.springernature.com.

Section `[Requests]` contains the default values for the requests library.

Simply edit this file using a simple text editor; changes will take effect the next time you start `sprynger`.  Remember to indent multi-line statements.
