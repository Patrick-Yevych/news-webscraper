from abc import ABC, abstractmethod
from typing import List


class Scraper(ABC):
    HEADERS = {'User-Agent': 'Mozilla/5.0'}

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