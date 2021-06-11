from typing import List
from bs4 import BeautifulSoup
import requests, re

HEADERS = {'User-Agent': 'Mozilla/5.0'}
STRS_BLACKLIST = ['×', 'Search tools', 'Recent', 'Sorted by relevance', 'SW_C_X', 'Sign in']
# Google supports 10 results per page for up to 1000 total results
PER_PAGE = 10 # default: 10
MAX_RES = 100 # default: 1000
GOOGLE_DATE_PATTERN = "^\d+ (seconds?|minutes?|hours?|days?|months?|years?) ago$"


def get_news_objs(query: str, page: int = 0) -> BeautifulSoup:
    req = requests.get('https://www.google.com/search?q='+query+'&source=lnms&tbm=nws&start='+str(page), allow_redirects=False, headers=HEADERS)
    return BeautifulSoup(req.text, 'html.parser')

def get_strs(news_objs: BeautifulSoup) -> List[str]:
    res = []
    for div in news_objs.find_all('div'):
        if div.string != None:
            res.append(div.string)
    return res

def get_spans(news_objs: BeautifulSoup) -> List[str]:
    res = []
    for span in news_objs.find_all('span'):
        if span.string != None:
            res.append(span.string)
    return res

def get_dates(query: str) -> List[str]:
    res = []
    for i in range(0, MAX_RES, PER_PAGE):
        spans = get_spans(get_news_objs(query, i))
        for span in spans:
            if re.match(GOOGLE_DATE_PATTERN, span) != None:
                res.append(span)
    return res

def get_headlines(query: str) -> List[str]: 
    res = []
    for i in range(0, MAX_RES, PER_PAGE): 
        strs = get_strs(get_news_objs(query, i))
        for t in strs:
            if t not in STRS_BLACKLIST:
                res.append(t)
    return res

def build_table(query: str) -> List[str]:
    res = []
    
    hdlnl = get_headlines(query)
    dates = get_dates(query)
    
    for i in range(0, min(len(hdlnl)-1, len(dates))):
        res.append([hdlnl[2*i+1], hdlnl[2*i], dates[i]])
    return res

print(build_table('bitcoin'))



# need to have date and url as well; url primary key
# scrap multiple search engines: bing, duckduck go.