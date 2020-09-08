# Reuters parsing
Parsing Reuters feed, store news to database, report news for given date.

## Installation

```
git clone https://github.com/ACauchy/reuters_parsing.git
cd reuters_parsing
./run.sh build
``` 

## Running

```
~/reuters_parsing# ./run.sh
Usage: run.sh {scrap|report|cleanup}
  -scrap: run scrapper, will scrap Reuters feed, db with schema will be provided automatically.
  -report <YYYY-DD-MM>: output news for given date into news-YYYY-DD-MM.csv (delimiter ;) into current dir
  -cleanup: stop all services and remove database data. USE CAREFULLY!
```


## Crontab
```
# Assume you have cloned repository into ~
~/reuters_parsing# crontab crontab
```