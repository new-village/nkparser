import logging
from abc import ABCMeta, abstractmethod

import requests
from bs4 import BeautifulSoup

# Set Logger
logger = logging.getLogger('NkLoader')

class NkLoader():
    def __init__(self):   
        return

    def load(self, category, entity_id):
        loader = self._create_loader(category)
        return loader.load_html(entity_id)
    
    def _create_loader(self, category):
        if category == "ENTRY":
            return EntryLoader()
        elif category == "ODDS":
            return OddsLoader()
        elif category == "HORSE":
            return HorseLoader()
        else:
            # Raise error and abort script
            logger.error('Unexpected category type: %s' % (category))
            raise SystemExit()


class BaseLoader(metaclass=ABCMeta):
    def load_html(self, entity_id):
        try:
            url = self.base_url + entity_id
            res = requests.get(url)
            res.encoding = 'EUC_JP'
            soup = BeautifulSoup(res.text, 'html.parser')
        except requests.exceptions as e:
            # Exception error handling
            logger.error('Request is failure: Name, server or service not known')
            logger.error('RequestsExceptions', e)
            raise SystemExit()

        # Response Status Confirmation
        if res.status_code not in [200]:
            # HTTP Response is not 200 (Normal)
            logger.error('Request to %s has been failure: %s' % (url, res.status_code))
            raise SystemExit()

        return self._confirm_data(soup)

    @abstractmethod
    def _confirm_data(self, soup):
        pass


class EntryLoader(BaseLoader):
    def __init__(self):
        self.base_url = 'https://race.netkeiba.com/race/shutuba.html?race_id='

    def _confirm_data(self, soup):
        if len(soup.select('div.RaceName')) == 0:
            soup = None
            logger.info('Race page is not found by defined race ID.')
            
        return soup


class OddsLoader(BaseLoader):
    def __init__(self):
        self.base_url = 'https://race.netkeiba.com/odds/index.html?type=b1&race_id='

    def _confirm_data(self, soup):
        if len(soup.select('div#odds_tan_block')) == 0:
            soup = None
            logger.info('Odds page is not found by defined race ID.')

        return soup


class HorseLoader(BaseLoader):
    def __init__(self):
        self.base_url = 'https://db.netkeiba.com/horse/'

    def _confirm_data(self, soup):
        if len(soup.select('div.horse_title > h1')) == 0:
            soup = None
            logger.info('Horse page is not found by defined horse ID.')

        return soup
