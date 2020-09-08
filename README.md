# Reuters parsing
Parsing Reuters feed, store news to database, report news for given date.

## Installation

```
git clone https://github.com/ACauchy/reuters.git
cd reuters
./run.sh build
``` 

## Running

```
~/reuters# ./run.sh
Usage: run.sh {scrap|report|cleanup}
  -scrap: run scrapper, will scrap Reuters feed (hardcoded), db with schema will be provided automatically.
  -report <YYYY-DD-MM>: output news for given date into news-YYYY-DD-MM.csv (delimiter ;) into current dir
  -cleanup: stop all services and remove database data. USE CAREFULLY!
```


## Crontab
```
# Assume you have cloned repository into ~
~/reuters# crontab crontab
```