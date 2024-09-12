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
>[MetadataRecord(contentType='Article', identifier='doi:10.1007/s10288-023-00561-5', language='en', ... ]

```py
book_metadata = Metadata('978-3-662-48847-8', start=1, max_results=3)
book_metadata.records_df[['title', 'language' ,'creators', 'abstract', 'subjects']]
```
<div style="font-size: 10px;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>title</th>
      <th>language</th>
      <th>creators</th>
      <th>abstract</th>
      <th>subjects</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Autonomous Vehicles and Autonomous Driving in ...</td>
      <td>en</td>
      <td>[(Flämig, Heike, None)]</td>
      <td>The degree of vehicle automation is continuous...</td>
      <td>[Engineering, Automotive Engineering, Engineer...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Effects of Autonomous Driving on the Vehicle C...</td>
      <td>en</td>
      <td>[(Winner, Hermann, None), (Wachenfeld, Walther...</td>
      <td>Since Carl Benz invented the automobile in 188...</td>
      <td>[Engineering, Automotive Engineering, Engineer...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Fundamental and Special Legal Questions for Au...</td>
      <td>en</td>
      <td>[(Gasser, Tom Michael, None)]</td>
      <td>The “Autonomous driving on the roads of the fu...</td>
      <td>[Engineering, Automotive Engineering, Engineer...</td>
    </tr>
  </tbody>
</table>
</div>

```py
book_metadata.facets_df.tail(5)
```
<div  style="font-size: 10px;">
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>facet</th>
      <th>value</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>6</th>
      <td>year</td>
      <td>2016</td>
      <td>32</td>
    </tr>
    <tr>
      <th>7</th>
      <td>country</td>
      <td>Germany</td>
      <td>24</td>
    </tr>
    <tr>
      <th>8</th>
      <td>country</td>
      <td>United States</td>
      <td>8</td>
    </tr>
    <tr>
      <th>9</th>
      <td>country</td>
      <td>France</td>
      <td>1</td>
    </tr>
    <tr>
      <th>10</th>
      <td>type</td>
      <td>Book</td>
      <td>32</td>
    </tr>
  </tbody>
</table>
</div>

