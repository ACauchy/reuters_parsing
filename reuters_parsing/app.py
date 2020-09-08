import csv
from datetime import datetime

import aiohttp

from .db import DBBackend
from .models import News
from .parser import Parser


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            raise aiohttp.ClientError(f'Bad response status == {response.status}')
        return await response.text()


async def scrap(url: str, parser: Parser, backend: DBBackend):
    async with aiohttp.ClientSession() as session:
        feed = parser.parse_feed(await fetch(session, url))
        with_text = [
            news._replace(text=parser.parse_news(await fetch(session, news.link)))
            for news in feed
        ]
    await backend.append_news(with_text)
    print("Done")


async def report(date_str: str, fn: str, backend: DBBackend):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Date format ({date_str}) is incorrect, use YYYY-MM-DD")
        return

    if fn is None:
        fn = f"News-{date_str}.csv"

    print(fn, end=' ')

    news = await backend.get_news(date)

    with open(fn, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(News._fields)
        for n in news:
            writer.writerow(n)

    print("Done")
