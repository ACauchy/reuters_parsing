from datetime import datetime
from typing import NamedTuple

__all__ = ['News']


class News(NamedTuple):
    title: str
    description: str
    link: str
    guid: str
    pub_date: datetime
    text: str = None
