from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from .models import News


class DBBackend(ABC):

    @abstractmethod
    def ensure_schema(self, force_recreate: bool):
        pass

    @abstractmethod
    def drop_schema(self):
        pass

    @abstractmethod
    async def init_engine(self):
        pass

    @abstractmethod
    async def stop_engine(self):
        pass

    @abstractmethod
    async def append_news(self, news: List[News]):
        pass

    @abstractmethod
    async def get_news(self, date: datetime) -> List[News]:  # sorted by pubdate
        pass
