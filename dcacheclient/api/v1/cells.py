"""

    User and administration interaction with dCache  # noqa: E501

"""

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

class cellsApi(object):
    """
    """

    def __init__(self, client):
        self.client = client

    
    def get_cells(self, **kwargs):
        """
        Provide information about all cells.  Requires admin role. Results sorted lexicographically by cell name.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/cells'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_cell_data(self, **kwargs):
        """
        Provide information about a specific cell.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/cells/{address}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_addresses(self, **kwargs):
        """
        Get a list of current addresses for well-known cells.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/cells/addresses'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    

