How to query ?
================

Querying the API follows the same pattern for all classes. Users can either do **string search**
or **specific field search** by passing keyword arguments. Here is an example:

.. code:: python

    >>> # String search: Query for documents containing the term "quantum" 
    >>> results = Meta('quantum')

    >>> # Specific field seach: Query for document belonging to the journal with the ISSN 3004-9261
    >>> results = Meta(issn='3004-9261')


There is the option to also pass both a query string and keyword arguments.

.. code:: python

    >>> # Query for documents containing the term "'quantum computing'" that where published in 2023
    >>> results = Metadata('"quantum computing"',
    >>>                     datefrom='2023-01-01',
    >>>                     dateto='2023-12-31')

Theoretically you can build the complete query as a string. The equivalent query to the above example would be:

.. code:: python

    >>> # Query for documents containing the term "'quantum computing'" that where published in 2023
    >>> results = Metadata('"quantum computing" datefrom:2023-01-01 dateto:2023-12-31')

Note that each element of the query is separated by a space and the field and values are separated by a colon. Spaces
are interpreted as an `AND` operator. The `OR` operator can be used by explicitly stating it.

.. code:: python

    >>> # Query for documents containing the term "'quantum computing'" or "'quantum information'"
    >>> results = OpenAccess('"quantum computing" OR "quantum information"')

Note that when the query string misses a specific field (e.g. `title`), the search will be performed in all fields.