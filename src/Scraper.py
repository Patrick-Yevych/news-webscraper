from abc import ABC, abstractmethod
from typing import List
import pandas as pd

"""
Abstract class which defines a web scraper that builds a table of 
news articles information with columns ['Headline', 'Source', 'URL', 'Date'].
"""
class Scraper(ABC):
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    COLUMNS = ['Headline', 'Source', 'URL', 'Date']

    """
    Postconditions:

    Retrieve a list of sources for each news article.
    """
    @abstractmethod
    def get_sources(self) -> List[str]: 
        pass

    """
    Postconditions:

    Retrieve a list of headlines for each news article.
    """
    @abstractmethod
    def get_headlines(self) -> List[str]: 
        pass

    """
    Postconditions:

    Retrieve a list of dates for each news article.
    """
    @abstractmethod
    def get_dates(self) -> List[str]: 
        pass

    """
    Postconditions:

    Retrieve a list of urls for each news article.
    """
    @abstractmethod
    def get_urls(self) -> List[str]:
        pass

    """
    Postconditions:

    Builds a table of news articles information with columns ['Headline', 'Source', 'URL', 'Date'].
    """
    @abstractmethod
    def build_table(self) -> pd.DataFrame:
        pass