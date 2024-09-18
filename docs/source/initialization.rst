Start-up
~~~~~~~~

You initalize `sprynger` as follows:

.. code-block:: python

    import sprynger
    sprynger.init()

This reads the configuration from the default locations. If you store the configuration file elsewhere, you can provide the path using keyword "config_dir" (str). You may also pass your own keys using the keyword "keys" (list).

In case you don't have a configuration file just enter your API key when prompted.



Configuration
~~~~~~~~~~~~~

`sprynger` stores values it needs for operation in a configuration file called `sprynger.cfg`. 
The config file saves credentials as well as directory names for folders that store downloaded results.
`sprynger` reads this file on startup.

You can find the configuration file in: `~/.config/sprynger/sprynger.cfg`

By default, after initial set-up (see below), the file will look like this:

.. code-block:: cfg

    [Directories]
    Metadata = home_dir/.cache/sprynger/metadata
    Meta = home_dir/.cache/sprynger/meta
    OpenAccess = home_dir/.cache/sprynger/open_access

    [Authentication]
    APIKey = XXX

    [Requests]
    Timeout = 20
    Retries = 5


Section `[Directories]` contains the paths where `sprynger` should store (cache) downloaded files.  `sprynger` will create them if necessary.

Section `[Authentication]` contains the API Keys which you obtain from https://dev.springernature.com.

Simply edit this file using a simple text editor; changes will take effect the next time you start `sprynger`.  Remember to indent multi-line statements.
