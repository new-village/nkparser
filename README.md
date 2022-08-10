# nkparser

**nkparser** is a python library for parsing [netkeiba.com](https://www.netkeiba.com/) data. nkparser only support to parse race (entry), odds, horse and results now.
Please note that this is a heavy load on the [netkeiba.com](https://www.netkeiba.com/) depending on your usage.
  

### Installing Requests and Supported Versions
----------------------
nkparser is available on pip installation.
```
$ python -m pip install git+https://github.com/new-village/nkparser.git
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

# Load ENTRY or RESULT
nkdata = nkparser.load("ENTRY", "201206050810")
print(nkdata.race)
# [{'race_id': '201206050810', 'race_number': 10, 'race_name': '有馬記念', ... }]
print(nkdata.table)
# [{'bracket': '7', 'horse_number': '13', 'horse_name': 'ゴールドシップ', ...}, ...]

# Load ODDS
nkdata = nkparser.load("ODDS", "201206050810")
print(nkdata.table)
# [{'horse_number': '1', 'tan': 51.6, 'fuku_min': 10.5, 'fuku_max': 18.7, 'race_id': '201206050810'}, ... ]
```
