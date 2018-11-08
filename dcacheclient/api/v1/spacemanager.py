"""

    User and administration interaction with dCache  # noqa: E501

"""

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)


class spacemanagerApi(object):
    """
    spacemanager Api class.
    """

    def __init__(self, client):
        self.client = client

    def get_tokens_for_group(self, **kwargs):
        """
        Get information about space tokens.  Requires admin role.  Results sorted by token id.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('id', 'voGroup', 'voRole', 'accessLatency', 'retentionPolicy', 'groupId', 'state', 'minSize', 'minFreeSpace')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/space/tokens'.format(**kwargs)
        response = self.client.call_api(
            kwargs,
            url,
            data=data,
            params=params,
            operation="get")
        return response

    def get_link_groups(self, **kwargs):
        """
        Get information about link groups.  Requires admin role. Results sorted lexicographically by link group name.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('name', 'id', 'onlineAllowed', 'nearlineAllowed', 'replicaAllowed', 'outputAllowed', 'custodialAllowed', 'voGroup', 'voRole', 'minAvailableSpace')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/space/linkgroups'.format(**kwargs)
        response = self.client.call_api(
            kwargs,
            url,
            data=data,
            params=params,
            operation="get")
        return response
