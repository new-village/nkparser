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

#### Entry (出走データ)
```python
>>> import nkparser
>>> nkdata = nkparser.load("entry", "201206050810")
>>> nkdata.info
[{'race_id': '201206050810', 'race_number': 10, 'race_name': '有馬記念', ... }]
>>> nkdata.table
[{'bracket': 7, 'horse_number': 13, 'horse_name': 'ゴールドシップ', ...}, {...}, ...]
```
  
#### Result (結果データ)
```python
>>> import nkparser
>>> nkdata = nkparser.load("result", "201206050810")
>>> nkdata.info
[{'race_id': '201206050810', 'race_number': 10, 'race_name': '有馬記念', ... }]
>>> nkdata.table
[{'rank': 1, 'horse_name': 'ゴールドシップ', 'rap_time': 151.9,...}, {...}, ...]
```
  
#### Odds (オッズデータ)
```python
>>> import nkparser
>>> nkdata = nkparser.load("odds", "201206050810")
>>> nkdata.table
[{'horse_number': 13, 'win': 2.7, 'show_min': 1.3, 'show_max': 1.5, ...}, {...}, ...]
```
  
#### Horse (血統データ/出走履歴データ)
```python
>>> import nkparser
>>> nkdata = nkparser.load("horse", "2009102739")
>>> nkdata.info
[{'horse_id': '2009102739', 'father_name': 'ステイゴールド', ... }]
>>> nkdata.table
[{'race_date': '20151227', 'race_name': '有馬記念', 'rank': 8, ...}, {...}, ...]
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
