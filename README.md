# sprynger
Simple API wrapper for the [Springer Nature APIs](https://dev.springernature.com).

## 🏔️ Overview Springer Nature
Springer Nature currently offers three APIs:
- **Springer Metadata API:** Metadata of articles, journal articles and book chapters.
- **Springer Meta API:** Advanced version offering versioned metadata.
- **Springer Open Access API:** Metadata and, where available, full-text

**Note:** sprynger currently supports the Metadata API

## 🪧 Example
### Metadata
```py
from sprynger import Metadata
```
```py
article_metadata = Metadata('10.1007/s10288-023-00561-5')
article_metadata.records
```
>[MetadataRecord(contentType='Article', identifier='doi:10.1007/s10288-023-00561-5', language='en', ...)]

```py
book_metadata = Metadata('978-3-662-48847-8', start=1, max_results=3)
book_metadata.results
```
> {'total': '32', 'start': '1', 'pageLength': '3', 'recordsDisplayed': '3'}

```py
journal_metadata = Metadata('1422-6952', start=5, max_results=10)
journal_metadata.facets
```
> [MetadataFacets(facet='subject', value='Mathematical Methods in Physics', count='1075'),
MetadataFacets(facet='subject', value='Physics', count='1075'),
MetadataFacets(facet='subject', value='Fluid- and Aerodynamics', count='1062'), ...]


## ⚠️ Disclaimer
This project is an independent API wrapper for the Springer Nature API. It is not affiliated with, endorsed, or maintained by Springer Nature. For official support, please refer to the Springers's [documentation](http://docs-dev.springernature.com/docs/) and support channels.
