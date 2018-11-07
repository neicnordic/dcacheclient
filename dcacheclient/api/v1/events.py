"""

    User and administration interaction with dCache  # noqa: E501

"""

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

class eventsApi(object):
    """
    """

    def __init__(self, client):
        self.client = client

    
    def channel_metadata(self, **kwargs):
        """
        Obtain metadata about a channel.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/channels/{id}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def delete(self, **kwargs):
        """
        Cancel a channel.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/channels/{id}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="delete")
        return response
    
    
    def modify(self, **kwargs):
        """
        Modify a channel.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        data = kwargs.get('body')
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/channels/{id}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="patch")
        return response
    
    
    def get_channels(self, **kwargs):
        """
        Obtain a list of channels.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ('client-id')
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/channels'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def register(self, **kwargs):
        """
        Request a new channel.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        data = kwargs.get('body')
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/channels'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="post")
        return response
    
    
    def channel_subscription(self, **kwargs):
        """
        Return the selector of this subscription.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/channels/{channel_id}/subscriptions/{type}/{subscription_id}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def delete(self, **kwargs):
        """
        Cancel a subscription.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/channels/{channel_id}/subscriptions/{type}/{subscription_id}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="delete")
        return response
    
    
    def subscribe(self, **kwargs):
        """
        Subscribe to events.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        data = kwargs.get('body')
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/channels/{id}/subscriptions/{type}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="post")
        return response
    
    
    def channel_subscriptions(self, **kwargs):
        """
        Obtain list a channel's subscriptions.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/channels/{id}/subscriptions'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_event_types(self, **kwargs):
        """
        Obtain a list of the available event types.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/eventTypes'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_selector_schema(self, **kwargs):
        """
        Obtain the JSON schema for this event type's selectors.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/eventTypes/{type}/selector'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_event_schema(self, **kwargs):
        """
        Obtain the JSON schema for events of this event type.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/eventTypes/{type}/event'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def service_metadata(self, **kwargs):
        """
        Obtain general information about event support in dCache.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    
    
    def get_event_type(self, **kwargs):
        """
        Obtain non-schema information about a specific event type.
        """
        LOGGER.debug('kwargs: %s' % str(kwargs))
        data = None
        params = {}
        attrs = ()
        for attr in attrs:
            params[attr] = kwargs.get(attr)
        url = self.client.url + '/api/v1' + '/events/eventTypes/{type}'.format(**kwargs)
        response = self.client.call_api(kwargs, url, data=data, params=params, operation="get")
        return response
    

