"""

    User and administration interaction with dCache  # noqa: E501

"""

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)


class alarmsApi(object):
    """
    alarms Api class.
    """

    def __init__(self, client):
        self.client = client

    def get_priority(self, **kwargs):
        """
        Request the current mapping of an alarm type to its priority. Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/alarms/priorities/{type}'.format(**kwargs)
        response = self.client.call_api(
            kwargs,
            url,
            data=data,
            params=params,
            operation="get")
        return response

    def get_alarms(self, **kwargs):
        """
        Provides a filtered list of log entries. Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('offset', 'limit', 'after', 'before', 'includeClosed', 'severity', 'type', 'host', 'domain', 'service', 'info', 'sort')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/alarms/logentries'.format(**kwargs)
        response = self.client.call_api(
            kwargs,
            url,
            data=data,
            params=params,
            operation="get")
        return response

    def bulk_update_or_delete(self, **kwargs):
        """
        Batch request to update or delete the indicated alarms. Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = kwargs.get('body')
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/alarms/logentries'.format(**kwargs)
        response = self.client.call_api(
            kwargs,
            url,
            data=data,
            params=params,
            operation="patch")
        return response

    def delete_alarm_entry(self, **kwargs):
        """
        Delete a specific log entry. Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/alarms/logentries/{key}'.format(**kwargs)
        response = self.client.call_api(
            kwargs,
            url,
            data=data,
            params=params,
            operation="delete")
        return response

    def update_alarm_entry(self, **kwargs):
        """
        Request to open or close the indicated log entry. Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = kwargs.get('body')
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/alarms/logentries/{key}'.format(**kwargs)
        response = self.client.call_api(
            kwargs,
            url,
            data=data,
            params=params,
            operation="patch")
        return response

    def get_priorities(self, **kwargs):
        """
        Request the current mapping of all alarm types to priorities. Requires admin role.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/alarms/priorities'.format(**kwargs)
        response = self.client.call_api(
            kwargs,
            url,
            data=data,
            params=params,
            operation="get")
        return response
