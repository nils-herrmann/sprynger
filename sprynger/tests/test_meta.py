"""Tests for the Meta class."""
from sprynger import init
from sprynger import Meta
from sprynger.utils.data_structures import (
    MetadataCreator,
    MetaDiscipline,
    MetadataFacets,
    MetaRecord,
    MetaURL,
)

init()

article = Meta(doi='10.1007/s00394-024-03496-7', refresh=True)

def test_results():
    """Test the results."""
    assert article.results.total == 1
    assert article.results.start == 1
    assert article.results.pageLength == 10
    assert article.results.recordsRetrieved == 1

def test_records():
    """Test the records."""
    expected_record = MetaRecord(
        contentType="Article",
        identifier="doi:10.1007/s00394-024-03496-7",
        language="en",
        urls=[
            MetaURL(
                format="html",
                platform="web",
                value="http://link.springer.com/openurl/fulltext?id=doi:10.1007/s00394-024-03496-7",
            ),
            MetaURL(
                format="pdf",
                platform="web",
                value="http://link.springer.com/openurl/pdf?id=doi:10.1007/s00394-024-03496-7",
            ),
            MetaURL(
                format="",
                platform="",
                value="http://dx.doi.org/10.1007/s00394-024-03496-7",
            ),
        ],
        title="Ultra-processed food intake in toddlerhood and mid-childhood in the UK: cross sectional and longitudinal perspectives",
        creators=[
            MetadataCreator(creator="Conway, Rana E.", ORCID="0000-0003-0955-7107"),
            MetadataCreator(creator="Heuchan, Gabriella N.", ORCID=None),
            MetadataCreator(creator="Heggie, Lisa", ORCID="0000-0002-4846-2357"),
            MetadataCreator(creator="Rauber, Fernanda", ORCID="0000-0001-9693-7954"),
            MetadataCreator(creator="Lowry, Natalie", ORCID="0000-0002-9137-5005"),
            MetadataCreator(creator="Hallen, Hannah", ORCID=None),
            MetadataCreator(creator="Llewellyn, Clare H.", ORCID="0000-0002-0066-2827"),
        ],
        publicationName="European Journal of Nutrition",
        openaccess=True,
        doi="10.1007/s00394-024-03496-7",
        publisher="Springer",
        publicationDate="2024-12-01",
        publicationType="Journal",
        issn="1436-6207",
        eIssn="1436-6215",
        volume=63,
        number=8,
        issueType="Regular",
        topicalCollection="",
        genre=["OriginalPaper", "Original Contribution"],
        startingPage=3149,
        endingPage=3160,
        journalId=394,
        onlineDate="2024-10-04",
        copyright="©2024 The Author(s)",
        abstract="Purpose (i) Characterize ultra-processed food (UPF) intakes in toddlerhood and mid-childhood, including identifying principal UPF sub-groups and associations with nutrient profile; (ii) explore stability and change in UPF intake between toddlerhood and mid-childhood. Methods Data were from children in the UK Gemini twin cohort at 21 months ( n \u2009=\u20092,591) and 7 years ( n \u2009=\u2009592) of age. UPF intakes were estimated using diet diaries and Nova classification. Complex samples general linear or logistic regression models were used to explore associations between UPF intake, UPF sub-groups and nutrients, and changes in intake over time. Results The contribution of UPF to total energy was 46.9% (±\u200914.7) at 21 months and 59.4% (±\u200912.5) at 7 years. Principal UPF sub-groups were yogurts, higher-fiber breakfast cereals, and wholegrain breads in toddlerhood, and puddings and sweet cereal products and white breads in mid-childhood. At both ages, mean free sugar and sodium intakes exceeded recommended maximums and higher UPF consumption was associated with consuming more of each nutrient ( P \u2009<\u20090.001). UPF intake was negatively associated with fat, saturated fat and protein intake in toddlerhood, and fiber intake in mid-childhood ( P \u2009<\u20090.001). Being in the highest UPF intake quintile in toddlerhood was predictive of being in the highest quintile in mid-childhood (OR 9.40, 95%CI 3.94–22.46). Conclusions UPF accounted for nearly half of toddlers’ energy, increasing to 59% in mid-childhood. Higher UPF consumers had higher intakes of free sugar and sodium. UPF intake in toddlerhood was predictive of mid-childhood intake. Effective policies are needed to reduce UPF intakes in the early years.",
        conferenceInfo=[],
        keyword=["Ultra-processed foods", "Diet quality", "Toddlers", "Children", "UK"],
        subjects=["Chemistry", "Nutrition"],
        disciplines=[MetaDiscipline(id="3524", term="Nutrition")],
    )
    assert article.records[0] == expected_record

def test_facets():
    """Test the facets."""
    assert len(article.facets) == 12

    expected_first_facet = MetadataFacets(facet='subject', value='Chemistry', count=1)
    assert article.facets[0] == expected_first_facet
