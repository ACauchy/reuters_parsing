from abc import ABC, abstractmethod
from typing import List

from .models import News


class Parser(ABC):
    @abstractmethod
    def parse_feed(self, feed: str) -> List[News]:
        pass

    @abstractmethod
    def parse_news(self, news: str) -> str:
        pass
