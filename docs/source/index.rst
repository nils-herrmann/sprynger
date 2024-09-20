.. sprynger documentation master file, created by
   sphinx-quickstart on Fri Sep 13 08:49:46 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

sprynger: API wrapper for Springer Nature
============================================

.. currentmodule:: sprynger

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

Retrieve metadata

.. code-block:: python

    article = DocumentMetadata('10.1007/s10660-023-09761-x')
    article.metadata

> MetadataRecord(contentType='Article', identifier='doi:10.1007/s10660-023-09761-x', language='en', ...)


.. code-block:: python

    book_metadata = Metadata('978-3-030-43582-0')
    for record in book_metadata:
        print(record)

> MetadataRecord(contentType='Chapter', title='Explanations of Machine Learning', abstract='There is an unavoidable tension...',...  
> MetadataRecord(contentType='Chapter', title='From Holmes to AlphaGo', abstract='Holmes’s enduring interest was in the...',...  
> ...

OpenAccess

.. code-block:: python

    from sprynger import OpenAccessArticle, OpenAccessChapter, OpenAccessJournal, OpenAccessBook

    article = OpenAccessArticle('10.1007/s10288-023-00561-5')
    article.paragraphs[0]

> OpenAcessParagraph(paragraph_id='Par2', ..., text='Continuing the first part of this paper, in which we provided a brief survey of the state of the art in multiple criteria decision aiding (MCDA)...')

.. code-block:: python

    journal = OpenAccessJournal('2198-6053')
    for article in journal:
        print(article.metadata)

> ArticleMeta(article_type='correction', language='en', publisher_id='s40747-0...  
> ArticleMeta(article_type='research-article', language='en', publisher_id='s40...  
> ...

.. code-block:: python

    book = OpenAccessBook("978-3-031-63500-7", start=1, max_results=2, refresh=30)
    for chapter in book:
        print(chapter.metadata)

> ChapterMeta(doi='10.1007/978-3-031-63501-4_13', chapter='13')  
> ChapterMeta(doi='10.1007/978-3-031-63501-4_18', chapter='18')

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
    classes/OpenAccessJournal.rst
    classes/OpenAccessBook.rst



