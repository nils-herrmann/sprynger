.. sprynger documentation master file, created by
   sphinx-quickstart on Fri Sep 13 08:49:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

sprynger: API wrapper for Springer Nature
============================================

Simple API wrapper for the `Springer Nature APIs <https://dev.springernature.com>`_

.. image:: https://badge.fury.io/py/sprynger.svg
    :target: https://pypi.org/project/sprynger/

.. image:: https://img.shields.io/pypi/pyversions/sprynger.svg
    :target: https://pypi.org/project/sprynger/

.. image:: https://readthedocs.org/projects/sprynger/badge/?version=latest
    :target: https://sprynger.readthedocs.io/en/latest/

.. image:: https://img.shields.io/pypi/dm/sprynger.svg
    :target: https://pypi.org/project/sprynger/

.. image:: https://img.shields.io/pypi/l/sprynger.svg
    :target: https://pypi.org/project/sprynger/

.. image:: https://api.codeclimate.com/v1/badges/1d053321a70d800bfc59/maintainability
    :target: https://codeclimate.com/github/your-repo/sprynger/maintainability


🏔️ Overview Springer Nature
----------------------------

Springer Nature currently offers three APIs:

- **Springer Metadata API:** Metadata of articles, journal articles and book chapters.
- **Springer Meta API:** Advanced version offering versioned metadata.
- **Springer OpenAccess API:** Metadata and, where available, full-text

**Note:** sprynger currently supports the Metadata and OpenAccess API


🪧 Example
----------

Import the classes and initialize the library:

.. code-block:: python

    from sprynger import Metadata, OpenAccessJournal, OpenAccessBook, init

    init()

Retrieve data by providing the identifier of the journal/article or book/chapter

.. code-block:: python

    article_metadata = Metadata('10.1007/s10288-023-00561-5')
    article_metadata.records

> [MetadataRecord(contentType='Article', identifier='doi:10.1007/s10288-023-00561-5', language='en', ...)]

.. code-block:: python

    journal = OpenAccessJournal('2198-6053')
    journal.article_meta[1]

> ArticleMeta(publisher_id='s40747-024-01487-z', manuscript='1487', doi='10.1007/s40747-024-01487-z')


.. currentmodule:: sprynger

🚀 Initialization
-----------------

.. toctree::
   :maxdepth: 1
   
   initialization.rst


📦 APIs
-------

.. toctree::
    :maxdepth: 1

    classes/Metadata.rst
    classes/OpenAccess.rst



