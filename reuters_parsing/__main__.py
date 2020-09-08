import argparse
import asyncio
import logging
import os
from datetime import datetime

import reuters_parsing.app as app
from .db_postgres import PostgresBackend
from .parser_reuters import ReutersParser

parser = argparse.ArgumentParser(description='Reuters web scrapper.', prog="python3.8 -m reuters_parsing")
parser.add_argument('-f', '--force-recreate', action='store_true', help="Recreate tables even if database not empty")

subparsers = parser.add_subparsers(help="Command to proceed.", dest='command')
scrap_parser = subparsers.add_parser('scrap', help="Do scraping of Reuters website and store new news into database. "
                                                   "Schema will be applied automatically (if database is empty "
                                                   "or --force-recreate specified).")

report_parser = subparsers.add_parser('report', help="Output news for given date into csv file.")
report_parser.add_argument('date', help="Date to report in YYYY-MM-DD format (in publisher timezone).")
report_parser.add_argument('file', nargs='?', help="File to store report, 'News-YYYY-MM-DD.csv' by default.")

parsed = parser.parse_args()

logging.basicConfig(level=logging.DEBUG if os.environ.get('APP_DEBUG', False) else logging.INFO)

dsn = "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" \
      "{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}".format(**os.environ)
backend = PostgresBackend(dsn)

backend.ensure_schema(parsed.force_recreate)


async def main():
    print("[{}]".format(datetime.now()), end=" ")
    await backend.init_engine()
    if parsed.command in [None, 'scrap']:
        print("scraping...")
        await app.scrap('http://feeds.reuters.com/reuters/topNews', ReutersParser(), backend)
    elif parsed.command == 'report':
        print("Reporting...")
        await app.report(parsed.date, parsed.file, backend)
    await backend.stop_engine()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
