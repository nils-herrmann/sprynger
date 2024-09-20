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
<div style="font-size: 12px;">

### Metadata
```py
from sprynger import DocumentMetadata, Metadata, init
init()
```
```py
article = DocumentMetadata('10.1007/s10660-023-09761-x')
article.metadata
```
> MetadataRecord(contentType='Article', identifier='doi:10.1007/s10660-023-09761-x', language='en', ...)

```py
book_metadata = Metadata('978-3-030-43582-0')
for record in book_metadata:
    print(record)
```
> MetadataRecord(contentType='Chapter', title='Explanations of Machine Learning', abstract='There is an unavoidable tension...',...  
> MetadataRecord(contentType='Chapter', title='From Holmes to AlphaGo', abstract='Holmes’s enduring interest was in the...',...  
> ...


### OpenAccess
```py
from sprynger import OpenAccessArticle, OpenAccessChapter, OpenAccessJournal, OpenAccessBook

article = OpenAccessArticle('10.1007/s10288-023-00561-5')
article.paragraphs[0]
```
> OpenAcessParagraph(paragraph_id='Par2', ..., text='Continuing the first part of this paper, in which we provided a brief survey of the state of the art in multiple criteria decision aiding (MCDA)...')

```py
journal = OpenAccessJournal('2198-6053')
for article in journal:
    print(article.metadata)
```
> ArticleMeta(article_type='correction', language='en', publisher_id='s40747-0...  
> ArticleMeta(article_type='research-article', language='en', publisher_id='s40...  
> ...

```py
book = OpenAccessBook("978-3-031-63500-7", start=1, max_results=2, refresh=30)
for chapter in book:
    print(chapter.metadata)
```
> ChapterMeta(doi='10.1007/978-3-031-63501-4_13', chapter='13')  
> ChapterMeta(doi='10.1007/978-3-031-63501-4_18', chapter='18')

</div>

## 📖 Documentation
For a comprehensive guide, see the documentation in [read the docs](https://sprynger.readthedocs.io/en/latest/index.html).

## ⭐️ Give the package a star
If the package helped you, give it a star!

## ⚠️ Disclaimer
This project is an independent API wrapper for the Springer Nature API. It is not affiliated with, endorsed, or maintained by Springer Nature. For official support, please refer to the Springers's [documentation](http://docs-dev.springernature.com/docs/) and support channels.
