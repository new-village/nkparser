# nkparser
[![Test](https://github.com/new-village/nkparser/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/new-village/nkparser/actions/workflows/unittest.yaml)
[![PyPI](https://badge.fury.io/py/nkparser.svg)](https://badge.fury.io/py/nkparser)  
**nkparser** is a python library for parsing [netkeiba.com](https://www.netkeiba.com/) data. nkparser only support to parse race (entry), odds, horse and results now.
Please note that this is a heavy load on the [netkeiba.com](https://www.netkeiba.com/) depending on your usage.
  

### Installing nkparser and Supported Versions
----------------------
nkparser is available on pip installation.
```
$ python -m pip install nkparser
```
nkparser officially supports Python 3.8+.
  
  
### Dependencies
----------------------
- [requests](https://docs.python-requests.org/en/latest/)
- [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)
- [jq](https://github.com/mwilliamson/jq.py)
  
### Usage
----------------------
To load [netkeiba.com](https://www.netkeiba.com/) data and parse to dictionay file.
```py
# import modules
import nkparser

# Load ENTRY
nkdata = nkparser.load("entry", "201206050810")
print(nkdata.info)
# [{'race_id': '201206050810', 'race_number': 10, 'race_name': '有馬記念', ... }]
print(nkdata.table)
# [{'bracket': 7, 'horse_number': 13, 'horse_name': 'ゴールドシップ', ...}, {...}, ...]

# Load ODDS
nkdata = nkparser.load("odds", "201206050810")
print(nkdata.table)
# [{'horse_number': 1, 'tan': 51.6, 'fuku_min': 10.5, 'fuku_max': 18.7, ...}, {...}, ...]

# Load RESULT
nkdata = nkparser.load("result", "201206050810")
print(nkdata.table)
# [{'bracket': 7, 'horse_number': 13, 'horse_name': 'ゴールドシップ', ...}, {...}, ...]

# Load HORSE
nkdata = nkparser.load("horse", "2009102739")
print(nkdata.info)
# [{'horse_id': '2009102739', 'father_name': 'ステイゴールド', ... }]
print(nkdata.table)
# [{'race_date': '20151227', 'race_name': '有馬記念', 'rank': 8, ...}, {...}, ...]
```
  
If you execute bulk data load, you can use `race_list` function.
```py
# import modules
import nkparser
# bulk load
for race_id in nkparser.race_list(2022, 7):
    nkdata = nkparser.load("entry", race_id)
```
  
This library generate `CREATE TABLE` sql for SQLite3.
```py
# import modules
import nkparser
# generate SQL
sql = nkparser.create_table_sql("entry")
print(sql)
# CREATE TABLE IF NOT EXISTS entry (bracket text, ... weight_diff integer);
```
