"""

    User and administration interaction with dCache  # noqa: E501

"""

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

class qosApi(object):
    """
    """

    def __init__(self, client):
        self.client = client

    
    def get_qos_list(self, **kwargs):
        """
        List the available quality of services for a specific object type.  Requires authentication.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/qos-management/qos/{type}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_queried_qos_for_files(self, **kwargs):
        """
        Provide information about a specific file quality of services.  Requires authentication.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/qos-management/qos/file/{qos}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_queried_qos_for_directories(self, **kwargs):
        """
        Provides information about a specific directory quality of services.  Requires authentication.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = kwargs['url'] + '/api/v1' + '/qos-management/qos/directory/{qos}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    

