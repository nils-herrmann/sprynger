"""Tests for the OpenAccess class."""
from sprynger import init, OpenAccess
from sprynger.openaccess import Article, Chapter
from sprynger.utils.data_structures import Affiliation, Contributor, Date, Reference, Section

init()

book = OpenAccess(isbn="978-3-031-63500-7", start=1, nr_results=2, refresh=30)
chapter = OpenAccess("doi:10.1007/978-3-031-61874-1_5", refresh=30)
chapter_with_text = OpenAccess(doi="10.1007/978-3-031-24498-8_7", refresh=30)
chapter_for_references = OpenAccess(doi='10.1007/978-3-031-63498-7_20')
book_pagination = OpenAccess(isbn='978-3-031-63498-7', nr_results=30, refresh=30)

journal = OpenAccess(issn="2198-6053", start=4, nr_results=3, refresh=30)
journal_pagination = OpenAccess('issn:2198-6584', nr_results=26, refresh=True)
article = OpenAccess(doi="10.1007/s40747-024-01577-y", refresh=30)


def test_article_abstract():
    """Test the abstract of the article."""
    expected_abstract = "Network traffic intrusion detection technology plays an important role in host and platform security. At present, machine learning and deep learning methods are often used for network traffic intrusion detection. However, the imbalance of relevant data sets will cause the model algorithm to learn the features of the majority categories and ignore the features of the minority categories, which will seriously affect the precision of network intrusion detection models. The number of samples of the attacks is much less than the number of normal samples. The classification performance on unbalanced data sets is poor and can not identify the minority attack samples well. To solve these problems, this paper proposed the resampling mechanism, which used random undersampling for the majority categories samples and K-Smote oversampling for the minority categories samples, so as to generate a more balanced data set and improve the model's detection rate for the minority categories. This paper proposed the Self-Attention with Gate (SAG) and BiGRU network model for intrusion detection on the CICIDS2017 data set, which can fully extract high-dimensional information from data samples and improve the detection rate of network attacks. The Self-Attention with Gate mechanism (SAG) based on the Transformer performed the feature extraction, filtered the irrelevant noise information, then extracted the long-distance dependency temporal sequence features by the BiGRU network, and obtained the classification results through the SoftMax classifier. Compared to the experimental results of other algorithms, such as Random Forest (RF) and BiGRU, it can be found that the overall classification precision for the SAG-BiGRU model in this paper is much higher and also has a good effect on the NSL-KDD data set."
    assert article[0].abstract == expected_abstract


def test_article_affiliations():
    """Test the affiliations of the article."""
    expected = [
        Affiliation(type=None, ref_nr='Aff1', ror='https://ror.org/04z7qrj66', grid='grid.412518.b', isni='0000 0001 0008 0619', division='College of Information Engineering', name='Shanghai Maritime University', city='Shanghai', country='China'),
        Affiliation(type=None, ref_nr='Aff2', ror='https://ror.org/05k2j8e48', grid='grid.495244.a', isni='0000 0004 1761 5722', division='College of Artificial Intelligence', name='Jiangxi University of Technology', city='Jiangxi', country='China'),
        Affiliation(type=None, ref_nr='Aff3', ror='https://ror.org/04z7qrj66', grid='grid.412518.b', isni='0000 0001 0008 0619', division='College of Merchant Marine', name='Shanghai Maritime University', city='Shanghai', country='China')
        ]
    for a in article:
        assert a.affiliations == expected


def test_article_contributors():
    """Test the contributors of the article."""
    expected = [
        Contributor(type='author', nr='Au1', orcid='http://orcid.org/0000-0002-1606-3511', surname='Hu', given_name='Zhanhui', email=None, affiliations_ref_nr=['Aff1']),
        Contributor(type='author', nr='Au2', orcid=None, surname='Liu', given_name='Guangzhong', email='gzhliu@shmtu.edu.cn', affiliations_ref_nr=['Aff1']),
        Contributor(type='author', nr='Au3', orcid=None, surname='Li', given_name='Yanping', email=None, affiliations_ref_nr=['Aff2']),
        Contributor(type='author', nr='Au4', orcid=None, surname='Zhuang', given_name='Siqing', email=None, affiliations_ref_nr=['Aff3'])
        ]
    for a in article:
        assert a.contributors == expected


def test_article_dates():
    """Test the dates of the article."""
    expected_date_accepted = Date(year=2024, month=7, day=21)
    expected_date_epub = Date(year=2024, month=9, day=9)
    expected_date_online = Date(year=2024, month=9, day=9)
    expected_date_ppub = Date(year=2024, month=12, day=None)
    expected_date_received = Date(year=2024, month=4, day=12)
    expected_date_registration = Date(year=2024, month=7, day=24)

    for a in article:
        assert a.date_accepted == expected_date_accepted
        assert a.date_epub == expected_date_epub
        assert a.date_online == expected_date_online
        assert a.date_ppub == expected_date_ppub
        assert a.date_received == expected_date_received
        assert a.date_registration == expected_date_registration


def test_article_full_text():
    """Test the full text of the article."""
    expected_start = '<body xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"><sec id="Sec1"><title>Introduction</title><p id="Par2">With the rapid development of computer Internet t'
    assert article[0].full_text.startswith(expected_start)
    
    expected_end = 'tion rate of the minority categories. The generalization ability of the training model for the minority attack categories is insufficient. We can continue to improve it in the future.</p></sec></body>'
    assert article[0].full_text.endswith(expected_end)


def test_article_meta():
    """Test the article meta-data."""
    for a in article:
        assert a.acknowledgements == 'We would like to express our gratitude and thank all the stakeholders: Professor Guangzhong Liu, Zhanhui Hu, Siqing Zhuang (Shanghai Maritime University), Yanping Li (Jiangxi University of Technology).'
        assert a.article_type == 'research-article'
        assert a.language == 'en'
        assert a.publisher_id == 's40747-024-01577-y'
        assert a.manuscript == '1577'
        assert a.doi == '10.1007/s40747-024-01577-y'
        assert a.title == 'SAGB: self-attention with gate and BiGRU network for intrusion detection'


def test_article_parsed_text():
    """Test the parsed text of an article."""
    assert len(article[0].parsed_text) == 18
    expected_paragraph = Section(section_id='Sec4',
                                 section_title='Data set',
                                 text='Data set In the paper, the data set is generated by Iman Sharafaldin et al. Canadian Security Agency, CICIDS2017 data set which contains the latest attack types, and the data error rate is close to zero, as shown in Table 1 . A total of 2,830,743 data samples is collected in the CICIDS2017 data set, among which the benign type data amount is 2,273,097, accounting for 80.3% of the total, and the remaining attack type data amount is 557,646, accounting for 19.7% of the total, which reflects that most of the network traffic is normal network data, containing only a small amount of attack data. In the CICIDS2017 data set, cyber attack types are grouped into 14 categories. Table\xa01 CICIDS2017 data set type distribution Category Quantity Proportion Benign 2,273,097 80.3004% DoS_Hulk 231,073 8.1630% PortScan 158,930 5.6144% DdoS 128,027 4.5227% Dos_GoldenEye 10,293 0.3636% FTP_Patator 7938 0.2804% SSH_Patator 5897 0.2083% Dos_Slowhttptest 5499 0.1943% Bot 1966 0.0695% Web_Attack_Brute_Force 1507 0.0532% Web_Attack_XSS 652 0.0230% Infiltration 36 0.0013% Web_Attack_Sql_Injection 21 0.0007% Heartbleed 11 0.0004% The CICIDS2017 data set contains eight CSV files, and each sample has 79 columns, including 78 feature columns and one label column in each CSV file. The data features of the data set include the average length of the packet, the maximum length of the packet, the total length of the Bwd packet, the destination port, and the number of packets with data labels.')
    assert article[0].parsed_text[3] == expected_paragraph


def test_article_references():
    """Test the references of the article."""
    expected_ref_last = Reference(
        ref_list_id="Bib1",
        ref_list_title="References",
        ref_id="CR42",
        ref_label="42.",
        ref_publication_type="journal",
        authors=["P Mishra", "V Varadharajan", "U Tupakula", "ES Pilli"],
        editors=[],
        names=[],
        ref_title="A detailed investigation and analysis of using machine learning techniques for intrusion detection",
        ref_source="IEEE Commun Surv Tutor",
        ref_year="2018",
        ref_doi="10.1109/comst.2018.2847722",
    )

    expected_ref_14 = Reference(
        ref_list_id="Bib1",
        ref_list_title="References",
        ref_id="CR15",
        ref_label="15.",
        ref_publication_type="other",
        authors=[],
        editors=[],
        names=[],
        ref_title="Rashid A, Siddique MJ, Ahmed SM (2020) Machine and deep learning based comparative analysis using hybrid approaches for intrusion detection system",
        ref_source=None,
        ref_year=None,
        ref_doi=None,
    )
    assert article[0].references[-1] == expected_ref_last
    assert article[0].references[14] == expected_ref_14


def test_book_meta():
    """Test the book meta data."""
    for chapter in book:
        assert chapter.book_doi == "10.1007/978-3-031-63501-4"
        assert chapter.publisher_id == "978-3-031-63501-4"
        assert chapter.book_title == "Automated Reasoning"
        assert chapter.book_title_id == "631234"
        assert chapter.book_sub_title == "12th International Joint Conference, IJCAR 2024, Nancy, France, July 3–6, 2024, Proceedings, Part II"
        assert chapter.book_pub_date == "2024-01-01"
        assert chapter.isbn_print == "978-3-031-63500-7"
        assert chapter.isbn_electronic == "978-3-031-63501-4"
        assert chapter.publisher_name == "Springer Nature Switzerland"
        assert chapter.publisher_loc == "Cham"


def test_chapter_abstract():
    """Test the abstract of the chapter."""
    expected_abstract = 'Feature Models (FMs) are not only an active scientific topic but they are supported by many tools from industry and academia. In this chapter, we provide an overview of example feature modelling tools and corresponding FM configurator applications. In our discussion, we first focus on different tools supporting the design of FMs. Thereafter, we provide an overview of tools that also support FM analysis. Finally, we discuss different existing FM configurator applications.'
    assert chapter[0].abstract == expected_abstract

    expected_abstract = 'Within a short space of time, the debate about Data Governance has fallen behind the realities of data driven industries and economies. The flow and trade of data is driven by the needs of different stake holders and evolution of global contexts of many technologies that are seen as local. To the Data Scientist, it may seem like an exciting time that has infinite possibility and opportunity to invent the near future. The gap between Data Governance on the African continent and Data practice poses a challenge that must be dealt with sooner than later. In this chapter I look at the intersection of Data Science practice and Data Governance and analyse some of the recent literature to identify areas of concern and focus. Ultimately, I want to look at how non-technical considerations are core in bridging Data Governance and Data Science practice. I borrow from other disciplines that had a head start with these challenges. Finally, I work to suggest steps that can be taken by practitioners to reduce this gap between governance and practice.'
    assert chapter_with_text[0].abstract == expected_abstract


def test_chapter_affiliations():
    """Test the affiliations of the chapter."""
    expected_affiliations = [
        Affiliation(type='book author', ref_nr='Aff1', ror='https://ror.org/00d7xrm67', grid='grid.410413.3', isni='0000 0001 2294 748X', division='Institute of Software Technology', name='Graz University of Technology', city='Graz', country='Austria'),
        Affiliation(type='book author', ref_nr='Aff2', ror=None, grid='grid.426094.d', isni='0000 0004 0625 6437', division='Corporate Technology', name='Siemens (Austria)', city='Wien', country='Austria'),
        Affiliation(type='book author', ref_nr='Aff3', ror='https://ror.org/03yxnpp24', grid='grid.9224.d', isni='0000 0001 2168 1229', division='ETS de Ingeniería Informática', name='University of Seville', city='Sevilla', country='Spain'),
        Affiliation(type=None, ref_nr='Aff4', ror='https://ror.org/00d7xrm67', grid='grid.410413.3', isni='0000 0001 2294 748X', division='Institute of Software Technology', name='Graz University of Technology', city='Graz', country='Austria'),
        Affiliation(type=None, ref_nr='Aff5', ror=None, grid='grid.426094.d', isni='0000 0004 0625 6437', division='Corporate Technology', name='Siemens (Austria)', city='Wien', country='Austria'),
        Affiliation(type=None, ref_nr='Aff6', ror='https://ror.org/03yxnpp24', grid='grid.9224.d', isni='0000 0001 2168 1229', division='ETS de Ingeniería Informática', name='University of Seville', city='Sevilla', country='Spain')
        ]
    for one_chapter in chapter:
        assert one_chapter.affiliations == expected_affiliations


def test_chapter_contributors():
    """Test the contributors of the chapter."""
    expected_contributors = [
        Contributor(type='author', nr=None, orcid=None, surname='Felfernig', given_name='Alexander', email='alexander.felfernig@ist.tugraz.at', affiliations_ref_nr=['Aff1']),
        Contributor(type='author', nr=None, orcid=None, surname='Falkner', given_name='Andreas', email='andreas.a.falkner@siemens.com', affiliations_ref_nr=['Aff2']),
        Contributor(type='author', nr=None, orcid=None, surname='Benavides', given_name='David', email='benavides@us.es', affiliations_ref_nr=['Aff3']),
        Contributor(type='author', nr=None, orcid=None, surname='Felfernig', given_name='Alexander', email=None, affiliations_ref_nr=['Aff4']),
        Contributor(type='author', nr=None, orcid=None, surname='Falkner', given_name='Andreas', email=None, affiliations_ref_nr=['Aff5']),
        Contributor(type='author', nr=None, orcid=None, surname='Benavides', given_name='David', email=None, affiliations_ref_nr=['Aff6'])
        ]
    for one_chapter in chapter:
        assert one_chapter.contributors == expected_contributors


def test_chapter_dates():
    """Test the dates of the chapter."""
    expected_date_epub = Date(year=2024, month=6, day=30)
    expected_date_online = Date(year=2024, month=6, day=30)
    expected_date_ppub = Date(year=None, month=None, day=None)
    expected_date_registration = Date(year=2024, month=5, day=27)

    for one_chapter in chapter:
        assert one_chapter.date_epub == expected_date_epub
        assert one_chapter.date_online == expected_date_online
        assert one_chapter.date_ppub == expected_date_ppub
        assert one_chapter.date_registration == expected_date_registration


def test_chapter_full_text():
    """Test the full text of the chapter."""
    expected_start = '<body xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"><sec id="Sec1"><title>Introduction</title><p id="Par2">The continued<index-term id="ITerm1"><term>Policy</term></index-term> rise of the information<index-term id="ITerm2"><term>Information</term></index-term><index-term id="ITerm3"><term>Data governance (DG)</term></index-term>economy<index-term id="ITerm4"><term>Data scientist</term></index-term> meant an increase in the use of data<index-term id="ITerm5"><term>Data</term></index-term> to build and deploy many data-driven products. These data-driven products are used to extract meaningful insights from raw information'
    assert chapter_with_text[0].full_text.startswith(expected_start)

    expected_end = 'rm> in ethics, fairness and mitigating abuse.</p></list-item></list></p></sec></body>'
    assert chapter_with_text[0].full_text.endswith(expected_end)


def test_chapter_meta():
    """Test the chapter meta data."""
    for one_chapter in chapter:
        assert one_chapter.acknowledgements is None
        assert one_chapter.doi == '10.1007/978-3-031-61874-1_5'
        assert one_chapter.chapter_nr == 5
        assert one_chapter.title == 'Tools and Applications'

    assert isinstance(book[0], Chapter)


def test_chapter_parsed_text():
    """Test the parsed text of a chapter."""
    assert len(chapter[0].parsed_text) == 0

    assert len(chapter_with_text[0].parsed_text) == 18
    expected_section = Section(section_id='Sec1',
                               section_title='Introduction',
                               text='Introduction The continued rise of the information economy meant an increase in the use of data to build and deploy many data-driven products. These data-driven products are used to extract meaningful insights from raw information , which is then used to address challenges across many different fields. This has coincided with the emergence and development of Data Science as a unique field of expertise, building data-driven products. Data Science is unique from Computer Science (the study of theory and practice of how computers work), and it encompasses many fields. From the perspective of users, the data-driven products have brought many new services and conveniences. In health, for example, there were rapid deployment of data tools to inform the public on the COVID-19 pandemic (Alamo et al., 2020 ; Shuja et al., 2021 ), pandemic prediction models (Ray et al., 2020 ) and estimations of impact of COVID-19 (Bradshaw et al., 2021 ). At the same time, some of the tools developed to deal with diagnostics/treatments were not as successful. An example of such data-driven products are the many tools/algorithms that were developed or deployed to improve radiology scans (Roberts et al., 2021 ; Wynants et al., 2020 ). On the one hand, one may be tempted to say such deployments were a complete failure. However, on the other hand these challenges highlight some of the shortcomings of data tools and areas of improvement. More importantly, these challenges outline the need to manage data (and its products) so that we take into account the human factors and impacts data may have across all domains. Keeping with the COVID-19 topic, the pandemic also put a spotlight on the lack of basic data infrastructure (Mbow et al., 2020 ), lack of data skills and/or lack of political will in many countries to focus on the improvement of data-driven products. These data-driven products and tools ultimately impact on the quality of responses to the pandemic. The aforementioned examples, highlight the need for Data Governance that takes a refined view of data in. I look at the Data Scientist (or Data Science Team) as the ones who make most of the decisions on the data tools they develop or create. This simplified view does not encapsulate all the challenges associated with what is currently taking place. It would be better to look at data-driven products through the lens of socio-technical systems. Socio-technical systems are systems which have interactions between humans, machines and the environment (Baxter & Sommerville, 2011 ). Even within the organization, the Data Science Team or Data Scientist cannot make decisions without a variety of different stakeholders, especially decisions that have an impact on humans and other environmental factors. As such, the Data Scientist should be able to understand the other inter-dependencies of organizations and society to better understand where they fit and that governance structures should exist to guide the development of systems with such inter dependencies. In this work, I aim to provide a better understanding of the governance /human factors that Data Scientist and organizations should be aware of. To address this challenge , I will answer fundamental research questions for the domain. Research Question: What are the salient points that Data Scientists should be aware of when it comes to Data Governance within organizations? Research Sub-Questions: Do the current policies or mechanisms on the African continent provide a coherent view that can be used by Data Scientists to navigate and respond appropriately to the needs of the organization. Can we learn from the ICT4D community to better understand how interventions should take care of more than just deploying a tool. It is important to contextualize why we need to answer these questions. We are at a time where policy is lagging deployment of data tools (this is discussed in this paper). This means there are gaps and blind spots that both Data Science practitioners and policy makers (both in public and private sectors) have. These blind spots have consequences. There has been much written about the data protection policy making and much written about Data Science practice and limitations. In this work I want to link the two in order to have a joint understanding that decision making has to be done together. The rest of the document is organized as follows. First, I look at the field of Data Science and how Data Governance fits into practice. The next step is to look at Data Governance on the African continent. I will set the scene and identify gaps that then intersect both areas of Data Science and Data Governance. In the proceeding section, I discuss how ICT4D may have already blazed a path that allows us to learn from in understanding the interactions of Data Science and Data Governance. The latter sections deal with the different stages of the Data Science process and proposals on how best Data Scientists can navigate human factors such as privacy, bias and security . Lastly, I conclude and summarize the viewpoints and evidence elaborated on in this paper.')
    assert chapter_with_text[0].parsed_text[0] == expected_section


def test_chapter_references():
    """Test the references of the chapter."""
    expected_ref_1 = Reference(
        ref_list_id='Bib1',
        ref_list_title='References',
        ref_id='CR1',
        ref_label='1.',
        ref_publication_type='other',
        authors=[],
        editors=[],
        names=[],
        ref_title='Beyersdorff, O., Hinde, L., Pich, J.: Reasons for hardness in QBF proof systems. ACM Trans. Comput. Theory 12(2), 10:1–10:27 (2020). https://doi.org/10.1145/3378665',
        ref_source=None,
        ref_year=None,
        ref_doi='10.1145/3378665',
    )
    expected_ref_2 = Reference(
        ref_list_id='Bib1',
        ref_list_title='References',
        ref_id='CR3',
        ref_label='3.',
        ref_publication_type='confproc',
        authors=['A Biere', 'F Lonsing', 'M Seidl'],
        editors=['N Bjørner', 'V Sofronie-Stokkermans'],
        names=[],
        ref_title='Blocked clause elimination for QBF',
        ref_source='Automated Deduction – CADE-23',
        ref_year='2011',
        ref_doi='10.1007/978-3-642-22438-6_10',
    )
    for one_chapter in chapter_for_references:
        assert one_chapter.references[0] == expected_ref_1
        assert one_chapter.references[2] == expected_ref_2
    
    assert chapter[0].references == []


def test_iterable():
    """Test the lengths"""
    assert len(book) == 2
    for book_chapter in book:
        assert isinstance(book_chapter, Chapter)

    assert len(journal) == 3
    for journal_article in journal:
        assert isinstance(journal_article, Article)


def test_journal_meta():
    """Test the journal meta-data."""
    for article in journal:
        assert article.journal_publisher_id == '40747'
        assert article.journal_doi is None
        assert article.journal_title == 'Complex & Intelligent Systems'
        assert article.journal_abbrev_title == 'Complex Intell. Syst.'
        assert article.issn_print == '2199-4536'
        assert article.issn_electronic == '2198-6053'
        assert article.publisher_name == 'Springer International Publishing'
        assert article.publisher_loc == 'Cham'


def test_pagination():
    """Test the pagination."""
    assert len(book_pagination) == 27
    dois = set([chapter.doi for chapter in book_pagination])
    assert len(dois) == 27

    assert len(journal_pagination) == 26
    dois = set([article.doi for article in journal_pagination])
    assert len(dois) == 26
