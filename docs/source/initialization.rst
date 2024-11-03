Start-up
========

You initalize `sprynger` as follows:

.. code:: python

    >>> import sprynger

    >>> sprynger.init(api_key='your key')

This reads your api key and uses the default configuration. You can also define `API_KEY` as an environment
variable. To use a custom configuration specify `config_file` in `init()`.

.. function:: init(api_key: Optional[str] = None, config_file: Optional[Union[str, Path]] = None) -> None

    Function to initialize the sprynger library. For more information go to the
    `documentation <file:///Users/nilsherrmann/sprynger/docs/build/html/initialization.html#configuration>`_.

    :param api_key: API key
    :type api_key: str, optional
    :param config_file: Path to the configuration .toml file.
    :type config_file: str or Path, optional

    :raises ValueError: If no API key was provided either as an argument or as an
        environment variable `API_KEY`.

    Example:

    .. code:: python

        from sprynger import init
        init(api_key='your key', config_file='path/to/custom/config.toml')


In case you don't have a configuration file just enter your API key when prompted.


Configuration
=============

The configuration file has to be a TOML file with the following structure. If any information is missing the default will be used.

.. code-block:: cfg

    [Directories]
    Metadata = /Users/user/.cache/sprynger/metadata
    Meta = /Users/user/.cache/sprynger/meta
    OpenAccess = /Users/user/.cache/sprynger/open_access

    [Requests]
    Timeout = 20
    Retries = 5
    BackoffFactor = 2.0


Section `[Directories]` contains the paths where `sprynger` should store (cache) downloaded files.  `sprynger` will create them if necessary.

Section `[Requests]` contains the default values for the requests library.
