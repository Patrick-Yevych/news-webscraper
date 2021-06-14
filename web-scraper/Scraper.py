from abc import ABC, abstractmethod
from typing import List
import pandas as pd


class Scraper(ABC):
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    COLUMNS = ['Headline', 'Source', 'URL', 'Date']

    @abstractmethod
    def get_sources(self) -> List[str]: 
        pass

    @abstractmethod
    def get_headlines(self) -> List[str]: 
        pass

    @abstractmethod
    def get_dates(self) -> List[str]: 
        pass

    @abstractmethod
    def get_urls(self) -> List[str]:
        pass

    @abstractmethod
    def build_table(self) -> pd.DataFrame:
        pass