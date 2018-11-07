"""

    User and administration interaction with dCache  # noqa: E501

"""

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

class poolsApi(object):
    """
    """

    def __init__(self, client):
        self.client = client

    
    def get_pool(self, **kwargs):
        """
        Get information about a specific pool (name, group membership, links). Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/pools/{pool}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_movers(self, **kwargs):
        """
        Get mover information for a specific pool.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('type', 'offset', 'limit', 'pnfsid', 'queue', 'state', 'mode', 'door', 'storageClass', 'sort')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/pools/{pool}/movers'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_queue_histograms(self, **kwargs):
        """
        Get histogram data concerning activity on a specific pool (48-hour window).
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/pools/{pool}/histograms/queues'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_files_histograms(self, **kwargs):
        """
        Get histogram data concerning file lifetime on a specific pool (60-day window).
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/pools/{pool}/histograms/files'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_pool_usage(self, **kwargs):
        """
        Get information about a specific pool (configuration, state, usage).  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/pools/{pool}/usage'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_repository_info_for_file(self, **kwargs):
        """
        Get information about a specific PNFS-ID usage within a specific pool.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/pools/{pool}/{pnfsid}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_nearline_queues(self, **kwargs):
        """
        Get nearline activity information for a specific pool.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('type', 'offset', 'limit', 'pnfsid', 'state', 'storageClass', 'sort')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/pools/{pool}/nearline/queues'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def kill_movers(self, **kwargs):
        """
        Kill a mover.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/pools/{pool}/movers/{id}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="delete")
        return response
    
    
    def update_mode(self, **kwargs):
        """
        Modify a pool's mode.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        data = kwargs.get('body')
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/pools/{pool}/usage/mode'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="patch")
        return response
    
    
    def get_pools(self, **kwargs):
        """
        Get information about all pools (name, group membership, links).  Requires admin role.  Results sorted lexicographically by pool name.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/pools'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_restores(self, **kwargs):
        """
        Obtain a (potentially partial) list of restore operations from some snapshot, along with a token that identifies the snapshot.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('token', 'offset', 'limit', 'pnfsid', 'subnet', 'pool', 'status', 'sort')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/restores'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    

