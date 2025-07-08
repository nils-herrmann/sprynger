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

.. image:: https://github.com/nils-herrmann/sprynger/actions/workflows/test.yml/badge.svg
   :target: https://github.com/nils-herrmann/sprynger/actions/workflows/test.yml

.. image:: https://codecov.io/gh/nils-herrmann/sprynger/graph/badge.svg?token=GF3FMVUWV3 
 :target: https://codecov.io/gh/nils-herrmann/sprynger

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
    >>> init(api_key='your free api key from https://dev.springernature.com')
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
    >>> # Retrieve full-text of three 'journal articles' with the keyword 'quantum computing' published before 2023
    >>> results = OpenAccess('"quantum computing"', dateto='2022-12-30', type='Journal Article', nr_results=3)
    >>> results.documents_found
    3515
    >>> for document in results:
    >>>    print(document.title)
    >>>    for section in document.parsed_text:
    >>>        print(section.text)
    'A neural network assisted' 
        'Introduction Quantum sensing 1  and metrology 2  are important branches of modern quantum technologi...'
        ...
    'Experimental demonstration of classical analogous time-dependent superposition of states'
        'Introduction The increased demand for quantum information science (QIS) and quantum computing 1 ,  2...'
        ...
    'A quantum-like cognitive approach to modeling human biased selection behavior'
        'Introduction With the advent of the Internet of Things and social networks, the reformation of the d...'
        ...

📝 Citation
-----------

If ``sprynger`` helped you retrieve your data, please cite the `corresponding paper <https://www.sciencedirect.com/science/article/pii/S2352711025001530>`_.

.. code-block:: bibtex

  @article{HERRMANN2025102186,
    title = {sprynger: Scriptable bibliometrics using a Python interface to Springer Nature},
    journal = {SoftwareX},
    volume = {31},
    pages = {102186},
    year = {2025},
    issn = {2352-7110},
    doi = {https://doi.org/10.1016/j.softx.2025.102186},
    url = {https://www.sciencedirect.com/science/article/pii/S2352711025001530},
    author = {Nils A. Herrmann and Michael E. Rose}
  }

.. documentation-end

📖 Documentation
-----------------

For a comprehensive guide, see the documentation in `read the docs <https://sprynger.readthedocs.io/en/stable/>`_.

⚠️ Disclaimer
--------------

This project is an independent API wrapper for the Springer Nature API.
It is not affiliated with, endorsed, or maintained by Springer Nature. For official support, please refer to the Springers's `documentation <http://docs-dev.springernature.com/docs/>`_ and support channels.
