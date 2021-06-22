from Scraper import Scraper

from typing import List
from bs4 import BeautifulSoup
import requests, re, time, datetime
import pandas as pd

STRS_BLACKLIST = ('×', 'Search tools', 'Recent', 'Sorted by relevance', 'SW_C_X', 'Sign in', 'Next >')
GOOGLE_LINK_PATTERN = r"^https?:\/\/.*\.google\..*$"

LINK_HEAD_PATTERN = r"(\/url\?q=)(https?:\/\/.*)"
GOOGLE_REL_DATE_PATTERN = r"^\d+ (seconds?|minutes?|hours?|days?|months?|years?) ago$"
GOOGLE_DATE_PATTERN = r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s\d{1,2},?\s\d{1,4}$"

class GoogleScraper(Scraper):

    page_step = 0
    max_pages = 0
    per_page = 0
    query = ""

    def __init__(self, query: str, max_pages: int = 100, page_step: int = 1, per_page: int = 10) -> None:
        self.query = query
        self.page_step = page_step
        self.max_pages = min(max_pages, 1000)
        self.per_page = min(per_page, 100)
    

    def get_news_objs(self, page: int = 0) -> BeautifulSoup:
        req = requests.get('https://www.google.com/search?q='+self.query.replace(" ", "+")+'&source=lnms&tbm=nws&start='+str(page)+'&num='+str(self.per_page), allow_redirects=False, headers=Scraper.HEADERS)
        return BeautifulSoup(req.text, 'html.parser')


    def get_strs(self, news_objs: BeautifulSoup) -> List[str]:
        res = []
        for div in news_objs.find_all('div'):
            if div.string != None:
                res.append(div.string)
        return res


    def get_spans(self, news_objs: BeautifulSoup) -> List[str]:
        res = []
        for span in news_objs.find_all('span'):
            if span.string != None:
                res.append(span.string)
        return res


    def get_href(self, news_objs: BeautifulSoup) -> List[str]:
        res = []
        for href in news_objs.find_all("a",href=re.compile(LINK_HEAD_PATTERN)):
            link = re.split(LINK_HEAD_PATTERN, href['href'])[2]
            if re.match(GOOGLE_LINK_PATTERN, link) == None:
                res.append(link)
        return res


    def get_rel_dates(self, news_objs: BeautifulSoup) -> List[str]:
        res = []
        for span in self.get_spans(news_objs):
            if re.match(GOOGLE_REL_DATE_PATTERN, span) != None:
                res.append(span)
        return res


    def get_urls(self) -> List[str]:
        res = []
        for i in range(0, self.max_pages, self.page_step):
            links = self.get_href(self.get_news_objs(i))
            for link in links:
                    res.append(link)
        return res


    def get_dates(self) -> List[str]:
        res = []
        for i in range(0, self.max_pages, self.page_step):
            for rd in self.get_rel_dates(self.get_news_objs(i)):
                date = None
                if re.match(GOOGLE_DATE_PATTERN, rd) != None:
                    text = rd.replace(",", "").replace(".", "")
                    date = datetime.datetime.strptime(text, '%b %d %Y')
                else:
                    text = rd.split(" ")
                    c = 0
                    if text[1] == "second" or text[1] == "seconds":
                        c = 1
                    elif text[1] == "minute" or text[1] == "minutes":
                        c = 60
                    elif text[1] == "hour" or text[1] == "hours":
                        c = 60*60
                    elif text[1] == "day" or text[1] == "days":
                        c = 24*60*60
                    elif text[1] == "month" or text[1] == "months":
                        c = 30*24*60*60
                    elif text[1] == "year" or text[1] == "years":
                        c = 12*30*24*60*60
                    date_list = (time.ctime(time.time()-c*int(text[0]))).split(" ") # Format ['Tue', 'Jun', '22', '04:34:42', '2021']
                    for d in date_list:
                        if d == '':
                            date_list.remove(d)
                    date = datetime.datetime.strptime(date_list[0]+" "+date_list[1]+" "+date_list[2]+" "+date_list[4], '%a %b %d %Y')
                print(date)
                res.append(date)
        return res


    def get_srcheads(self) -> List[str]: 
        res = []
        for i in range(0, self.max_pages, self.page_step): 
            for t in self.get_strs(self.get_news_objs(i)):
                if t not in STRS_BLACKLIST:
                    res.append(t)
        return res

    def get_sources(self) -> List[str]:
        res = []
        srcheads = self.get_srcheads()
        for i in range(0, len(srcheads), 2):
            res.append(srcheads[i+1])
        return res

    def get_headlines(self) -> List[str]:
        res = []
        srcheads = self.get_srcheads()
        for i in range(0, len(srcheads), 2):
            res.append(srcheads[i])
        return res

    def build_table(self) -> pd.DataFrame:
        lst = []
        
        hdlns = self.get_headlines()
        srcs = self.get_sources()
        dates = self.get_dates()
        urls = self.get_urls()[::2]
        
        for i in range(0, min(len(srcs), len(hdlns), len(dates), len(urls))):
            lst.append([hdlns[i], srcs[i], urls[i], dates[i]])

        return pd.DataFrame(lst, columns=Scraper.COLUMNS)
