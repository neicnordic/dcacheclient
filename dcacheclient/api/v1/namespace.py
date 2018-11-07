"""

    User and administration interaction with dCache  # noqa: E501

"""

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

class namespaceApi(object):
    """
    """

    def __init__(self, client):
        self.client = client

    
    def get_file_attributes(self, **kwargs):
        """
        Find metadata and optionally directory contents.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('children', 'locality', 'locations', 'qos', 'limit', 'offset')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/namespace/{path}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def cmr_resources(self, **kwargs):
        """
        Modify a file or directory.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        data = kwargs.get('body')
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/namespace/{path}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="post")
        return response
    
    
    def delete_file_entry(self, **kwargs):
        """
        delete a file or directory
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/namespace/{path}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="delete")
        return response
    
    
    def get_attributes(self, **kwargs):
        """
        Discover information about a file from the PNFS-ID.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/id/{pnfsid}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    

    def bring_online(self, path):
        return self.cmr_resources(
            url=self.client.url,
            path=path,
            body='{"action": "qos", "target": "disk+tape"}')
