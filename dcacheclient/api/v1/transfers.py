"""

    User and administration interaction with dCache  # noqa: E501

"""

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)


class transfersApi(object):
    """
    transfers Api class.
    """

    def __init__(self, client):
        self.client = client

    def get_transfers(self, **kwargs):
        """
        Provide a list of all client-initiated transfers that are either queued or currently running.  Internal (pool-to-pool) transfers are excluded.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('token', 'offset', 'limit', 'state', 'door', 'domain', 'prot', 'uid', 'gid', 'vomsgroup', 'pnfsid', 'pool', 'client', 'sort')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/transfers'.format(**kwargs)
        response = self.client.call_api(
            kwargs,
            url,
            data=data,
            params=params,
            operation="get")
        return response
