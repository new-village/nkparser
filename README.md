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
  
### Usage
----------------------
To load [netkeiba.com](https://www.netkeiba.com/) data and parse to dictionay file.
```py
# import modules
from nkparser import load
from nkparser import parse

# Load HTML (ex. ENTRY, ODDS, HORSE)
loader = load.NkLoader()
entry_soup = loader.load('ENTRY', "201206050810")
odds_soup = loader.load('ODDS', "201206050810")
horse_soup = loader.load('HORSE', "2009102739")

# Parse HTML
parser = parse.NkParser()
race = parser.parse('RACE', entry_soup)
entry = parser.parse('ENTRY', entry_soup)
```
