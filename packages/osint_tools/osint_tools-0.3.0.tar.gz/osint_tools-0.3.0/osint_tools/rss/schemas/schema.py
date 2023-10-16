from .config import BaseConfig
from enum import Enum, auto
from typing import Optional
import re
from uuid import uuid4
from pydantic import root_validator, Field
import strawberry

'''
published:  Fri, 04 Mar 2022 23:20:00 +0000
published_parsed:  time.struct_time(tm_year=2022, tm_mon=3, tm_mday=4, tm_hour=23, tm_min=20, tm_sec=0, tm_wday=4, tm_yday=63, tm_isdst=0)
authors:  [{'name': 'Tyler Durden'}]
author:  Tyler Durden
author_detail:  {'name': 'Tyler Durden'}
id:  731160 at https://www.zerohedge.com
guidislink:  False
title:  Coinbase CEO: "Ordinary Russians Are Using Crypto As A Lifeline"
title_detail:  {
    'type': 'text/plain', 
    'language': None, 
    'base': 'https://cms.zerohedge.com/', 
    'value': 'Coinbase CEO: "Ordinary Russians Are Using Crypto As A Lifeline"'}
links:  [{'rel': 'alternate', 'type': 'text/html', 'href': 'https://www.zerohedge.com/crypto/coinbase-ceo-ordinary-russians-are-using-crypto-lifeline'}]
link:  https://www.zerohedge.com/crypto/coinbase-ceo-ordinary-russians-are-using-crypto-lifeline
summary:  <span class="field field--name-title field--type-string field--label-hidden">Coinbase CEO: "Ordinary Russians Are Using Crypto As A Lifeline"</span>

[{'author': 'Tyler Durden',
  'id': '733984 at https://www.zerohedge.com',
  'link': 'https://www.zerohedge.com/political/photos-show-miami-beach-transformed-ghost-town-after-curfews',
  'links': [{'href': 'https://www.zerohedge.com/political/photos-show-miami-beach-transformed-ghost-town-after-curfews',
             'rel': 'alternate',
             'type': 'text/html'}],
  'published': 'Sun, 27 Mar 2022 18:00:00 +0000',
  'title': "Photos Show Miami Beach Transformed Into Ghost Town After 'Spring "
           "Break' Curfews"}]

  'summary_detail': {'base': 'https://cms.zerohedge.com/',
                     'language': None,
                     'type': 'text/html',
                     'value': '<span class="field field--name-title '
                              'field--type-string field--label-hidden">How The '
                              "West's Ban On Russian Gold Could "
                              'Backfire</span>
'''

class EnumBase(Enum):
    @classmethod
    def list_name_or_value(cls, name_or_value: str) -> list[str]:
        """list names or values of derived enum class

        Args:
            name_or_value (str): name  | value

        Returns:
            (list[str]): list of derived enum classes names or values
        """
        return [getattr(i, name_or_value) for i in cls.__members__.values()]

    @classmethod
    def list_values_to_titlecase(cls):
        def to_title_case(s):
            return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)
        return [to_title_case(i.value.replace('_', ' ')) for i in cls.__members__.values()]


class EnumAutoBase(EnumBase):
    def _generate_next_value_(name, start, count, last_values):
        return name

@strawberry.enum
class EnumRSS(str, EnumBase):
    cbc_world = 'cbc.ca/cmlink/rss-world'
    cbc_health = 'https://rss.cbc.ca/lineup/health.xml'
    full_rss = 'https://www.zerohedge.com/fullrss2.xml'
    # zh = 'http://feeds.feedburner.com/zerohedge/feed'
    pf = 'https://www.reddit.com/r/ActualPublicFreakouts.rss'
    cnn = 'http://rss.cnn.com/rss/cnn_topstories.rss'
    # York Times Home Page
    nyt = 'http://feeds.nytimes.com/nyt/rss/HomePage'
    nyt_daily = 'https://feeds.simplecast.com/54nAGcIl'
    
    the_atlantic = 'https://www.theatlantic.com/feed/all'
    
    nbc_news = 'http://www.wthr.com/Global/category.asp?C=79076&clienttype=rss'
    # washhington Post: Today's Highlights
    wp = 'http://www.washingtonpost.com/rss/'
    # Top U.S. News
    ap = 'https://www.apnews.com/apf-usnews'
    # TODAY.com News - Top Stories
    usat = 'http://rssfeeds.usatoday.com/usatoday-NewsTopStories'
    #  Topics: News
    npr = 'http://www.npr.org/rss/rss.php?id=1001'
    #  News - Americas: World Edition
    # ps://www.bbc.co.uk/news/10628494#userss
    bbc = 'http://newsrss.bbc.co.uk/rss/newsonline_world_edition/americas/rss.xml'
    # ps://www.cbc.ca/rss/

    ctv_canada = 'http://ctvnews.ca/rss/Canada'
    ctv_politics = 'http://www.ctvnews.ca/rss/Politics'
    ctv_top = 'http://ctvnews.ca/rss/TopStories'
    ctv_bc = 'http://bc.ctvnews.ca/rss/bcnews'
    ctv_calgary = 'http://calgary.ctvnews.ca/rss/CalgaryNews'
    ctv_toronto = 'http://toronto.ctvnews.ca/rss/Latest'
    ctv_atlantic = 'http://atlantic.ctvnews.ca/rss/Atlantic'

    # https://www.thetelegraph.com/rss/
    telegraph = 'https://www.thetelegraph.com/rss/feed/News-RSS-Feed-1978.php'

    yahoo_news = 'https://news.yahoo.com/rss/'

    # https://www.dailymail.co.uk/home/article-2684527/RSS-Feeds.html
    daily_mail_latest = 'https://www.dailymail.co.uk/articles.rss'
    daily_mail_health = 'https://www.dailymail.co.uk/health/index.rss'
    daily_mail_science = 'https://www.dailymail.co.uk/sciencetech/index.rss'
    daily_mail_az = 'https://www.dailymail.co.uk/news/astrazeneca/index.rss'
    daily_mail_asia = 'https://www.dailymail.co.uk/news/asia/index.rss'
    dm_bill_gates = 'https://www.dailymail.co.uk/news/bill-gates/index.rss'
    dm_canada = 'https://www.dailymail.co.uk/news/canada/index.rss'
    dm_covid = 'https://www.dailymail.co.uk/news/coronavirus/index.rss'
    dm_depression = 'https://www.dailymail.co.uk/news/depression/index.rss'

    dm_fbi = 'https://www.dailymail.co.uk/news/fbi/index.rss'
    dm_giz_lane = 'https://www.dailymail.co.uk/news/ghislainemaxwell/index.rss'
    haaretz = 'https://www.haaretz.com/srv/haaretz-latest-headlines'



@strawberry.enum
class Topic(str, EnumAutoBase):
    UN_ASSIGNED = auto()

@strawberry.enum
class PropCategory(str, EnumAutoBase):
    COVERUP = auto()
    PROP_AGANDA = auto()
    CO_ORDINATED = auto()
    UN_CATEGORIZED = auto()


class Authors(BaseConfig):
    name: Optional[str] = None

class AuthorDetail(Authors):
    pass

class TitleDetail(BaseConfig):
    base: Optional[str] = None
    language: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None
    class Config:
        schema_extra = {
            'type': 'text/plain', 
            'language': None, 
            'base': 'https://cms.zerohedge.com/', 
            'value': 'Coinbase CEO: "Ordinary Russians Are Using Crypto As A Lifeline"'
        }

class Links(BaseConfig):
    rel: Optional[str] = None
    type: Optional[str] = None
    href: Optional[str] = None

    class Config:
        schema_extra = {
            'example': {
                'links': [
                    {
                        'rel': 'alternate', 
                        'type': 'text/html', 
                        'href': 'https://www.zerohedge.com/crypto/coinbase-ceo-ordinary-russians-are-using-crypto-lifeline'
                    }
                ]   
            }
        }

class MediaCredit(BaseConfig):
    content: Optional[str] = None


class MediaContent(BaseConfig):
    medium: Optional[str] = None
    url: Optional[str] = None
    height: Optional[str] = None
    width: Optional[str] = None
    type: Optional[str] = None

class Tags(BaseConfig):
    term: Optional[str] = None
    scheme: Optional[str] = None
    label: Optional[str] = None


class SummaryDetail(TitleDetail):
    '''SummaryDetail has same fields as TitleDetail'''
    pass

class RSS_Schema(BaseConfig):
    id: str = Field(default_factory=uuid4, alias="_id")# type: ignore
    unique_id: Optional[str] = Field('')
    authors: Optional[list[Authors]] = None
    author: Optional[str] = None
    author_detail: Optional[AuthorDetail] = None
    credit: Optional[str] = None
    media_credit: Optional[list[MediaCredit]] = None
    title: Optional[str] = None
    link: Optional[str] = None
    links: Optional[list[Links]] = None
    published: Optional[str] = None
    tags: Optional[list[Tags]] = None
    media_content: Optional[list[MediaContent]] = None
    summary_detail: Optional[SummaryDetail] = None
    flag: PropCategory = PropCategory.UN_CATEGORIZED
    topic: Topic = Topic.UN_ASSIGNED
    is_sorted: bool = False
    rss_url: str

    @root_validator(pre=True)
    def create_uid(cls, val):
        # gql wants alias _id not model name id
        val['unique_id'] = str(val['rss_url']) + '-' + str(val['link'])
        return val

@strawberry.experimental.pydantic.type(
    model=Authors, 
    all_fields=True)
class AuthorsGQL:
    pass

@strawberry.experimental.pydantic.type(
    model=AuthorDetail, 
    all_fields=True)
class AuthorDetailGQL:
    pass

@strawberry.experimental.pydantic.type(
    model=TitleDetail, 
    all_fields=True)
class TitleDetailGQL:
    pass

@strawberry.experimental.pydantic.type(
    model=Tags, 
    all_fields=True)
class TagsGQL:
    pass

@strawberry.experimental.pydantic.type(
    model=MediaCredit, 
    all_fields=True)
class MediaCreditGQL:
    pass

@strawberry.experimental.pydantic.type(
    model=MediaContent, 
    all_fields=True)
class MediaContentGQL:
    pass


@strawberry.experimental.pydantic.type(
    model=Links, 
    all_fields=True)
class LinksGQL:
    pass

@strawberry.experimental.pydantic.type(
    model=SummaryDetail, 
    all_fields=True)
class SummaryDetailGQL:
    pass

@strawberry.experimental.pydantic.type(
    model=RSS_Schema, 
    all_fields=True)
class RSS_SchemaGQL:
    pass


