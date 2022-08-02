'''load.py
'''
import json
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
    @abstractmethod
    def load_html(self, entity_id):
        ''' load_html
        '''

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

    def _create_url(self, base_url, entity_id):
        return base_url.replace('{ID}', entity_id)

class EntryLoader(BaseLoader):
    ''' EntryLoader
    '''
    def load_html(self, entity_id):
        ''' load_html
        '''
        base_url = 'https://race.netkeiba.com/race/shutuba.html?race_id={ID}'
        return self._requests(self._create_url(base_url, entity_id))

class OddsLoader(BaseLoader):
    ''' OddsLoader
    '''
    def load_html(self, entity_id):
        ''' load_html
        '''
        # Load JSON Data
        base_url = 'https://race.netkeiba.com/api/api_get_jra_odds.html?race_id={ID}&type=1&action=init'
        text = json.loads(self._requests(self._create_url(base_url, entity_id)))

        # Confirme Data Format
        if text['status'] == 'middle':
            # HTTP Response is not 200 (Normal)
            logger.warning('There is no odds data: %s', entity_id)
            raise SystemExit()

        text.update({'race_id': entity_id})
        return json.dumps(text)

class HorseLoader(BaseLoader):
    ''' HorseLoader
    '''
    def load_html(self, entity_id):
        ''' load_html
        '''
        base_url = 'https://db.netkeiba.com/horse/{ID}'
        return self._requests(self._create_url(base_url, entity_id))
