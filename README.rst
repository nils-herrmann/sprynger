.. documentation-begin

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
- **Springer OpenAccess API:** Metadata and, where available, full-text.


⬇️ Install
-----------
Download and install the package from PyPI:

.. code-block:: bash

    pip install sprynger


🪧 Example Use
---------------

.. code:: python
    
    >>> from sprynger import Meta, OpenAccess, init
    >>> init()
    >>>
    >>> # Get metadata of all chapters in the book with ISBN '978-3-031-63497-0'
    >>> book_metadata = Metadata(isbn='978-3-031-63497-0', nr_results=3)
    >>> for chapter in book_metadata:
    >>>     print(chapter.identifier)
    >>>     print(chapter.abstract)
    'doi:10.1007/978-3-031-63498-7_20'
        'Modern solvers for quantified Boolean formulas (QBFs) process formulas in prenex form, ...'
    'doi:10.1007/978-3-031-63498-7_9'
        'Given a finite consistent set of ground literals, we present an algorithm that generates ...'
    'doi:10.1007/978-3-031-63498-7_3'
        'The TPTP World is a well established infrastructure that supports research, development, ...'
    >>> # Print the facets of the retrieved chapter's metadata
    >>> book_metadata.facets
    [MetadataFacets(facet='subject', value='Artificial Intelligence', count='27'),...]
    >>> 
    >>> # Retrieve full-text of 'journal articles' with the keyword 'quantum computing' published before 2023
    >>> results = OpenAccess('"quantum computing"', dateto='2022-12-30', type='Journal Article', nr_results=3)
    >>> results.documents_found
    4350
    >>> for document in results:
    >>>    print(document.title)
    >>>    print(document.paragraphs[0].text)
    'A neural network assisted' 
        'A versatile magnetometer must deliver a readable response when exposed to target fields ...'
    'Experimental demonstration of classical analogous time-dependent superposition of states'
        'One of the quantum theory concepts on which quantum information processing stands is superposition ...'
    'A quantum-like cognitive approach to modeling human biased selection behavior'
        'Cognitive biases of the human mind significantly influence the human decision-making process ...'

.. documentation-end