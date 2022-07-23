# nkparser

**nkparser** is a python library for parsing [netkeiba.com](https://www.netkeiba.com/) data. nkparser only support to parse race (entry), odds, horse and results now.
Please note that this is a heavy load on the [netkeiba.com](https://www.netkeiba.com/) depending on your usage.
  

### Installing Requests and Supported Versions
----------------------
nkparser is available on pip installation.
```
$ python -m pip install git+https://github.com/karaage0703/unko
```
Requests officially supports Python 3.8+.
  
  
### Dependencies
----------------------
- [requests](https://docs.python-requests.org/en/latest/)
- [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)
  
### Usage
----------------------
To parse netkeiba data and convert to pandas dataframe.
```py
# import modules
from netkeiba import load

# load bs4 (ex. RACE)
loader = load.NetkeibaLoader()
soup = loader.load('RACE', "202202011211")
```  
