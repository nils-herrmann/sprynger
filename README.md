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

## 🪧 Example
### Metadata
```py
from sprynger import Metadata, OpenAccessJournal, OpenAccessBook, init

init()
```
```py
article_metadata = Metadata('10.1007/s10288-023-00561-5')
article_metadata.records
```
>[MetadataRecord(contentType='Article', identifier='doi:10.1007/s10288-023-00561-5', language='en', ...)]

```py
journal_metadata = Metadata('1422-6952', start=5, max_results=10)
journal_metadata.facets
```
> [MetadataFacets(facet='subject', value='Mathematical Methods in Physics', count='1075'),
MetadataFacets(facet='subject', value='Physics', count='1075'),
MetadataFacets(facet='subject', value='Fluid- and Aerodynamics', count='1062'), ...]

### OpenAccess
```py
journal = OpenAccessJournal('2198-6053', cache=True, refresh=False)
journal.journal_meta
```
> JournalMeta(publisher_id='40747', doi=None, journal_title='Complex & Intelligent Systems', journal_abbrev_title='Complex Intell. Syst.', issn_print='2199-4536', ...)

```py
journal.article_meta[1]
```
> ArticleMeta(publisher_id='s40747-024-01487-z', manuscript='1487', doi='10.1007/s40747-024-01487-z')

```py
journal.paragraphs[1]
```
> [OpenAcessParagraph(paragraph_id='Par2', section_id='Sec1', section_title='Introduction', text='Facing the ...,
 OpenAcessParagraph(paragraph_id='Par3', section_id='Sec1', section_title='Introduction', text='In order ...,
...]
```py
book = OpenAccessBook("978-3-031-63500-7", start=1, max_results=2, refresh=30)
book.paragraphs[1]
```
[OpenAcessParagraph(paragraph_id='Par2', section_id='Sec1', section_title='Introduction', text='The characterisation of ...,
OpenAcessParagraph(paragraph_id='Par3', section_id='Sec1', section_title='Introduction', text='Establishing ...,...]

## 📖 Documentation
For a comprehensive guide, see the documentation in [read the docs](https://sprynger.readthedocs.io/en/latest/index.html).

## ⚠️ Disclaimer
This project is an independent API wrapper for the Springer Nature API. It is not affiliated with, endorsed, or maintained by Springer Nature. For official support, please refer to the Springers's [documentation](http://docs-dev.springernature.com/docs/) and support channels.
