"""
dCache client library.
"""

import requests
import logging

from dcacheclient import oidc
from dcacheclient.api.v1 import alarms
from dcacheclient.api.v1 import billing
from dcacheclient.api.v1 import cells
from dcacheclient.api.v1 import identity
from dcacheclient.api.v1 import namespace
from dcacheclient.api.v1 import poolmanager
from dcacheclient.api.v1 import pools
from dcacheclient.api.v1 import qos
from dcacheclient.api.v1 import spacemanager
from dcacheclient.api.v1 import transfers
from dcacheclient.api.v1 import events
from dcacheclient.common.utils import full_path

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)


class Client(object):
    """
    Client for the dCache API.
    """

    def __init__(self, url, session=None, username=None, password=None, certificate=None,
                 private_key=None, x509_proxy=None, no_check_certificate=True,
                 ca_certificate=None, ca_directory=None, timeout=None,
                 oidc_agent_account=None, version="v1"):
        """
        :param string url: A user-supplied endpoint URL for the dCache service.
                           http(s)://$HOST:$PORT/
        :param session: A session object to be used for communication. If one is
                    not provided it will be constructed from the provided
                    kwargs. (optional)
        :param username: user name to authenticate as.
        :param password: password to authenticate with.
        :param certificate: Client certificate file to connect on SSL server
                            requiring SSL client certificate.
        :param cert_key: Client certificate private key file.
        :param cert_key: Client certificate private key file.
        :param x509_proxy:  Client X509 proxy file.
        :param no_check_certificate: Allow to access servers without checking SSL certs.
                         The server's certificate will not be verified.
        :param ca_certificate: CA certificate to verify peer against (SSL).
        :param ca_directory: CA directory to verify peer against (SSL).
        :param timeout: socket read timeout value, passed directly to the requests library.
        :param oidc_agent_account: the oidc-agent account name from which to get the access token.
        :param string version: The version of API to use.
        """
        self.url = url
        self.username = username
        self.password = password
        self.certificate = certificate
        self.private_key = private_key
        self.x509_proxy = x509_proxy
        self.no_check_certificate = no_check_certificate
        self.ca_certificate = ca_certificate
        self.ca_directory = ca_directory
        self.timeout = timeout

        if not session:
            self.session = requests.Session()

            if self.username and self.password:
                LOGGER.debug('HTTP basic authentication: %s' % (self.username))
                self.session.auth = (self.username + '#admin', self.password)

            if oidc_agent_account:
                self.session.auth = oidc.OidcAuth(oidc_agent_account)

            if self.certificate and self.private_key:
                LOGGER.debug('HTTPS X.509 grid authentication: (%s,%s)' % (self.certificate, self.private_key))
                self.session.cert = (
                    full_path(self.certificate),
                    full_path(self.private_key))
#            else:
#                LOGGER.debug('ANONYMOUS authentication')

            if self.x509_proxy:
                LOGGER.debug('HTTPS X.509 grid proxy authentication: %s' % (self.x509_proxy))
                self.session.cert = full_path(self.x509_proxy)

            if self.no_check_certificate:
                LOGGER.debug('no_check_certificate: False')
                self.session.verify = False
            elif self.ca_certificate:
                LOGGER.debug('CA certificate: %s' % self.ca_certificate)
                self.session.verify = self.ca_certificate
            elif self.ca_directory:
                LOGGER.debug('CA directory: %s' % self.ca_directory)
                self.session.verify = self.ca_directory

            self.timeout = timeout
        else:
            self.session = session

        self.alarms = alarms.alarmsApi(client=self)
        self.billing = billing.billingApi(client=self)
        self.cells = cells.cellsApi(client=self)
        self.identity = identity.identityApi(client=self)
        self.namespace = namespace.namespaceApi(client=self)
        self.poolmanager = poolmanager.poolmanagerApi(client=self)
        self.pools = pools.poolsApi(client=self)
        self.qos = qos.qosApi(client=self)
        self.spacemanager = spacemanager.spacemanagerApi(client=self)
        self.transfers = transfers.transfersApi(client=self)
        self.events = events.eventsApi(client=self)

    def call_api(self, args, url, operation='get', params=None, data=None):
        '''
        '''
        operation_mapping = {
            'put': self.session.put,
            'get': self.session.get,
            'post': self.session.post,
            'delete': self.session.delete,
            'head': self.session.head,
            'options': self.session.options,
            'patch': self.session.patch}
        LOGGER.debug('operation: %s', operation)
        LOGGER.debug('url: %s', url)
        LOGGER.debug('session.cert: %s', self.session.cert)
        LOGGER.debug('params: %s', params)
        LOGGER.debug('data: %s', data)
        response = operation_mapping[operation](
            url,
            params=params,
            json=data,
            timeout=self.timeout)
        LOGGER.debug('response.url: %s', response.url)
        LOGGER.debug('response.headers: %s', response.headers)
        LOGGER.debug('response.status_code: %d', response.status_code)
        LOGGER.debug('response.text: %s', response.text)

        if operation in ('get') and response.status_code == 200:
            return response.json()

        if operation in ('post') and response.status_code == 201:
            return response

        LOGGER.error('response.status_code: %d', response.status_code)
        LOGGER.error('response.text: %s', response.text)
        return False

    def close(self):
        self.session and self.session.close()
