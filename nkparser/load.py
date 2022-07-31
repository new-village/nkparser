'''load.py
'''
import logging
from abc import ABCMeta, abstractmethod

import requests


# Set Logger
logger = logging.getLogger('NkLoader')

class NkLoader():
    ''' NkLoader
    '''
    def __init__(self):
        return

    def load(self, category, entity_id):
        ''' load
        '''
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
            logger.error('Unexpected category type: %s', category)
            raise SystemExit()


class BaseLoader(metaclass=ABCMeta):
    ''' BaseLoader
    '''
    def load_html(self, entity_id):
        ''' load_html
        '''
        return self._requests(self._create_url(entity_id))

    def _requests(self, url):
        try:
            response = requests.get(url)
            response.encoding = response.apparent_encoding
        except requests.exceptions.RequestException as exp:
            # Exception error handling
            logger.error('Request is failure: Name, server or service not known')
            raise SystemExit() from exp

        # Response Status Confirmation
        if response.status_code not in [200]:
            # HTTP Response is not 200 (Normal)
            logger.error('Request to %s has been failure: %s', url, response.status_code)
            raise SystemExit()

        return response.text

    @abstractmethod
    def _create_url(self, entity_id):
        pass


class EntryLoader(BaseLoader):
    ''' EntryLoader
    '''
    def _create_url(self, entity_id):
        base_url = 'https://race.netkeiba.com/race/shutuba.html?race_id={ID}'
        return base_url.replace('{ID}', entity_id)

class OddsLoader(BaseLoader):
    ''' OddsLoader
    '''
    def _create_url(self, entity_id):
        base_url = 'https://race.netkeiba.com/api/api_get_jra_odds.html?race_id={ID}&type=1'
        return base_url.replace('{ID}', entity_id)

class HorseLoader(BaseLoader):
    ''' HorseLoader
    '''
    def _create_url(self, entity_id):
        base_url = 'https://db.netkeiba.com/horse/{ID}'
        return base_url.replace('{ID}', entity_id)
