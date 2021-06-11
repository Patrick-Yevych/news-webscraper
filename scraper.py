from typing import List
from bs4 import BeautifulSoup
import requests

STRS_BLACKLIST = ['×', 'Search tools', 'Recent', 'Sorted by relevance', 'SW_C_X', 'Sign in']
# Google supports 10 results per page for up to 1000 total results
PER_PAGE = 10 # default: 10
MAX_RES = 100 # default: 1000

def get_news_objs(query: str, page: int) -> BeautifulSoup:
    req = requests.get('https://www.google.com/search?q='+query+'&source=lnms&tbm=nws&start='+str(page), allow_redirects=False)
    return BeautifulSoup(req.text, 'html.parser')

def get_strs(news_objs: BeautifulSoup) -> List[str]:
    res = []
    for div in news_objs.find_all('div'):
        if div.string != None:
            res.append(div.string)
    return res

def get_headlines(query: str): 
    x = []
    for i in range(0, MAX_RES, PER_PAGE): 
        strs = get_strs(get_news_objs(query, i))
        for t in strs:
            if t not in STRS_BLACKLIST:
                x.append(t)
    # pair titles and source
    res = []
    for i in range(0, len(x)-1, 2):
        res.append([x[i+1], x[i]])
    return res
print (get_headlines('bitcoin'))

# need to have date and url as well; url primary key
# scrap multiple search engines: bing, duckduck go.