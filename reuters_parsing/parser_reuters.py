from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from .models import *
from .parser import Parser


class ReutersParser(Parser):
    class ParseError(Exception):
        pass

    # noinspection PyMethodMayBeStatic
    def parse_feed(self, feed: str) -> List[News]:
        bs = BeautifulSoup(feed, "xml")

        items = bs.find_all('item')
        if not items:
            raise ReutersParser.ParseError()

        try:
            return [
                News(
                    str(i.find('title').text),
                    str(i.find('description').text),
                    str(i.find('link').text),
                    str(i.find('guid').text),
                    datetime.strptime(
                        str(i.find('pubDate').text),
                        "%a, %d %b %Y %H:%M:%S %z"
                    ).replace(tzinfo=None),
                ) for i in items]
        except (AttributeError, ValueError) as e:
            raise ReutersParser.ParseError(e)

    def parse_news(self, news: str) -> str:
        bs = BeautifulSoup(news, "lxml")
        try:
            # noinspection PyUnresolvedReferences
            return bs.find('div', attrs={'class': 'StandardArticleBody_body'}).text
        except AttributeError as e:
            raise ReutersParser.ParseError(e)
