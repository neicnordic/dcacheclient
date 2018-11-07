"""

    User and administration interaction with dCache  # noqa: E501

"""

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

class billingApi(object):
    """
    """

    def __init__(self, client):
        self.client = client

    
    def get_data(self, **kwargs):
        """
        Request the time series data for a particular specification. The available specifications can be obtained via GET on histograms/grid/description.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/billing/histograms/{key}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_p2ps(self, **kwargs):
        """
        Provides a list of pool-to-pool transfers for a specific PNFS-ID.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('before', 'after', 'limit', 'offset', 'serverPool', 'clientPool', 'client', 'sort')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/billing/p2ps/{pnfsid}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_reads(self, **kwargs):
        """
        Provides a list of read transfers for a specific PNFS-ID.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('before', 'after', 'limit', 'offset', 'pool', 'door', 'client', 'sort')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/billing/reads/{pnfsid}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_restores(self, **kwargs):
        """
        Provide a list of tape reads for a specific PNFS-ID.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('before', 'after', 'limit', 'offset', 'pool', 'sort')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/billing/restores/{pnfsid}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_stores(self, **kwargs):
        """
        Provides a list of tape writes for a specific PNFS-ID.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('before', 'after', 'limit', 'offset', 'pool', 'sort')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/billing/stores/{pnfsid}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_writes(self, **kwargs):
        """
        Provides a list of write transfers for a specific PNFS-ID.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('before', 'after', 'limit', 'offset', 'pool', 'door', 'client', 'sort')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/billing/writes/{pnfsid}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_grid(self, **kwargs):
        """
        Provides the list of available histograms with their corresponding identifer.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/billing/histograms/grid/description'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_grid_data(self, **kwargs):
        """
        Provide the full "grid" of time series data in one pass. Data is sorted lexicographically by key.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/billing/histograms'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    

