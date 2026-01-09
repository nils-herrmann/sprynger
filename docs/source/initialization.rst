Start-up
========

You initalize `sprynger` as follows:

.. code:: python

    >>> import sprynger

    >>> # Use a single API key (for backward compatibility)
    >>> sprynger.init(api_key='your key')
    
    >>> # Or use separate keys for Meta and OpenAccess APIs
    >>> sprynger.init(api_key_meta='your_meta_key', api_key_oa='your_openaccess_key')

This reads your api key(s) and uses the default configuration. You can also define environment 
variables: ``API_KEY`` (for both APIs), ``API_KEY_META`` (for Meta API), or ``API_KEY_OA`` 
(for OpenAccess API). To use a custom configuration specify `config_file` in `init()`.

.. function:: init(api_key: Optional[str] = None, api_key_meta: Optional[str] = None, api_key_oa: Optional[str] = None, config_file: Optional[Union[str, Path]] = None) -> None

    Function to initialize the sprynger library. For more information go to the
    `documentation <file:///Users/nilsherrmann/sprynger/docs/build/html/initialization.html#configuration>`_.

    :param api_key: API key (for backward compatibility, will be used for both Meta and OpenAccess)
    :type api_key: str, optional
    :param api_key_meta: API key for Meta API
    :type api_key_meta: str, optional
    :param api_key_oa: API key for OpenAccess API
    :type api_key_oa: str, optional
    :param config_file: Path to the configuration .toml file.
    :type config_file: str or Path, optional

    :raises ValueError: If no API key was provided either as an argument or as 
        environment variables (``API_KEY``, ``API_KEY_META``, or ``API_KEY_OA``).

    Example:

    .. code:: python

        from sprynger import init
        # Use a single key for both APIs
        init(api_key='your key')
        # Use separate keys
        init(api_key_meta='your_meta_key', api_key_oa='your_openaccess_key')
        # Use a custom configuration file
        init(api_key='your key', config_file='path/to/custom/config.toml')


In case you don't have a configuration file just enter your API key when prompted.

.. note::

    **Springer Nature API Changes**: Springer Nature has changed its authentication system. 
    Users now receive separate API keys for the **Meta** and **OpenAccess** APIs. 
    The **Metadata API is being discontinued**. Use the **Meta API** instead for versioned metadata.
    
    - If you have a single key that works for both APIs, use ``api_key='your_key'``
    - If you have separate keys, use ``api_key_meta='meta_key'`` and ``api_key_oa='oa_key'``
    
    **Environment Variables**: You can also set API keys via environment variables:
    
    - ``API_KEY`` - Used as default for both Meta and OpenAccess APIs
    - ``API_KEY_META`` - Specific key for Meta API (overrides ``API_KEY``)
    - ``API_KEY_OA`` - Specific key for OpenAccess API (overrides ``API_KEY``)


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
