# sprynger
Simple API wrapper for the [Springer Nature APIs](https://dev.springernature.com).

![PyPI version](https://badge.fury.io/py/sprynger.svg)
![Python versions](https://img.shields.io/pypi/pyversions/sprynger.svg)
![Documentation Status](https://readthedocs.org/projects/sprynger/badge/?version=latest)
![Downloads](https://img.shields.io/pypi/dm/sprynger.svg)
![License](https://img.shields.io/pypi/l/sprynger.svg)
![Maintainability](https://api.codeclimate.com/v1/badges/1d053321a70d800bfc59/maintainability)

## 🏔️ Overview Springer Nature
Springer Nature currently offers three APIs:
- **Springer Metadata API:** Metadata of articles, journal articles and book chapters.
- **Springer Meta API:** Advanced version offering versioned metadata.
- **Springer OpenAccess API:** Metadata and, where available, full-text

**Note:** sprynger currently supports the Metadata and OpenAccess API

## ⬇️ Install

Download and install the package from PyPI:
```bash
pip install sprynger
```

## 🪧 Example Use
<div style="font-size: 12px;">

### Metadata

```python
from sprynger import Metadata, init

init()

book_metadata = Metadata(isbn='978-3-031-63497-0', nr_results=3)
for chapter in book_metadata:
    print(chapter.identifier)
    print(chapter.abstract)
```
>doi:10.1007/978-3-031-63498-7_20
>> Modern solvers for quantified Boolean formulas (QBFs) process formulas in prenex form, ...

>doi:10.1007/978-3-031-63498-7_9
>>Given a finite consistent set of ground literals, we present an algorithm that generates ...

>doi:10.1007/978-3-031-63498-7_3
>> The TPTP World is a well established infrastructure that supports research, development, ...



```python
book_metadata.facets
```
>[MetadataFacets(facet='subject', value='Artificial Intelligence', count='27'),...]


### OpenAccess

```python
from sprynger import OpenAccess
```


```python
results = OpenAccess('"quantum computing"',
                     dateto='2022-12-30',
                     type='Journal Article',
                     nr_results=3)
```


```python
results.documents_found
```
> 4350

```python
for document in results:
    print(document.title)
    print(document.paragraphs[0].text)
```
> A neural network assisted 
>> A versatile magnetometer must deliver a readable response when exposed to target fields ...

> Experimental demonstration of classical analogous time-dependent superposition of states
>> One of the quantum theory concepts on which quantum information processing stands is superposition ...

> A quantum-like cognitive approach to modeling human biased selection behavior
>> Cognitive biases of the human mind significantly influence the human decision-making process ...

<div>

## 📖 Documentation
For a comprehensive guide, see the documentation in [read the docs](https://sprynger.readthedocs.io/en/latest/index.html).

## ⭐️ Give the package a star
If the package helped you, give it a star!

## ⚠️ Disclaimer
This project is an independent API wrapper for the Springer Nature API. It is not affiliated with, endorsed, or maintained by Springer Nature. For official support, please refer to the Springers's [documentation](http://docs-dev.springernature.com/docs/) and support channels.
