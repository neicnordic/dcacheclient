"""

    User and administration interaction with dCache  # noqa: E501

"""

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

class poolmanagerApi(object):
    """
    """

    def __init__(self, client):
        self.client = client

    
    def get_pool_groups(self, **kwargs):
        """
        Get a list of poolgroups.  Requires admin role. Results sorted lexicographically by group name.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/poolgroups'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_pool_group(self, **kwargs):
        """
        Get information about a poolgroup.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/poolgroups/{group}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_pools_of_group(self, **kwargs):
        """
        Get a list of pools that are a member of a poolgroup.  If no poolgroup is specified then all pools are listed. Results sorted lexicographically by pool name.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/poolgroups/{group}/pools'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_group_usage(self, **kwargs):
        """
        Get usage metadata about a specific poolgroup.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/poolgroups/{group}/usage'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_queue_info(self, **kwargs):
        """
        Get pool activity information about pools of a specific poolgroup.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/poolgroups/{group}/queues'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_space_info(self, **kwargs):
        """
        Get space information about pools of a specific poolgroup.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/poolgroups/{group}/space'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_queue_histograms(self, **kwargs):
        """
        Get aggregated pool activity histogram information from pools in a specific poolgroup.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/poolgroups/{group}/histograms/queues'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_files_histograms(self, **kwargs):
        """
        Get aggregated file statistics histogram information from pools in a specific poolgroup.  Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/poolgroups/{group}/histograms/files'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_links(self, **kwargs):
        """
        Get information about all links.  Requires admin role. Results sorted lexicographically by link name.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/links'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_link_groups(self, **kwargs):
        """
        Get information about all linkgroups.  Requires admin role. Results sorted lexicographically by link group name.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/links/groups'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_partitions(self, **kwargs):
        """
        Get information about all partitions.  Requires admin role. Results sorted lexicographically by partition name.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/partitions'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def match(self, **kwargs):
        """
        Describe the pools selected by a particular request.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('type', 'store', 'dcache', 'net', 'protocol', 'linkGroup')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/pool-preferences'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_units(self, **kwargs):
        """
        List all units.  Requires admin role. Results sorted lexicographically by unit name.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/units'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_unit_groups(self, **kwargs):
        """
        List all unitgroups.  Requires admin role. Results sorted lexicographically by unit group name.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/units/groups'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    

