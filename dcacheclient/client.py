"""
dDcache client library.
"""



class Connection(object):

    """
    Convenience class to make requests that will also retry the request
    Requests will have an X-Auth-Token header whose value is either
    the preauthtoken or a token obtained from the auth service using
    the user credentials provided as args to the constructor. If
    os_options includes a service_username then requests will also have
    an X-Service-Token header whose value is a token obtained from the
    auth service using the service credentials. In this case the request
    url will be set to the storage_url obtained from the auth service
    for the service user, unless this is overridden by a preauthurl.
    """

    def __init__(self, authurl=None, user=None, key=None, retries=5,
                 preauthurl=None, preauthtoken=None, snet=False,
                 starting_backoff=1, max_backoff=64, tenant_name=None,
                 os_options=None, auth_version="1", cacert=None,
                 insecure=False, cert=None, cert_key=None,
                 ssl_compression=True,
                 timeout=None, session=None, force_auth_retry=False):
        """
        :param authurl: authentication URL
        :param user: user name to authenticate as
        :param key: key/password to authenticate with
        :param retries: Number of times to retry the request before failing
        :param preauthurl: storage URL (if you have already authenticated)
        :param preauthtoken: authentication token (if you have already
                             authenticated) note authurl/user/key/tenant_name
                             are not required when specifying preauthtoken
        :param snet: use SERVICENET internal network default is False
        :param starting_backoff: initial delay between retries (seconds)
        :param max_backoff: maximum delay between retries (seconds)
        :param auth_version: OpenStack auth version, default is 1.0
        :param tenant_name: The tenant/account name, required when connecting
                            to an auth 2.0 system.
        :param os_options: The OpenStack options which can have tenant_id,
                           auth_token, service_type, endpoint_type,
                           tenant_name, object_storage_url, region_name,
                           service_username, service_project_name, service_key
        :param insecure: Allow to access servers without checking SSL certs.
                         The server's certificate will not be verified.
        :param cert: Client certificate file to connect on SSL server
                            requiring SSL client certificate.
        :param cert_key: Client certificate private key file.
        :param ssl_compression: Whether to enable compression at the SSL layer.
                                If set to 'False' and the pyOpenSSL library is
                                present an attempt to disable SSL compression
                                will be made. This may provide a performance
                                increase for https upload/download operations.
        :param retry_on_ratelimit: by default, a ratelimited connection will
                                   raise an exception to the caller. Setting
                                   this parameter to True will cause a retry
                                   after a backoff.
        :param timeout: The connect timeout for the HTTP connection.
        :param session: A keystoneauth session object.
        :param force_auth_retry: reset auth info even if client got unexpected
                                 error except 401 Unauthorized.
        """
        self.session = session
        self.authurl = authurl
        self.user = user
        self.key = key
        self.retries = retries
        self.http_conn = None
        self.attempts = 0
        self.snet = snet
        self.starting_backoff = starting_backoff
        self.max_backoff = max_backoff
        self.auth_version = auth_version
        self.os_options = dict(os_options or {})
        if tenant_name:
            self.os_options['tenant_name'] = tenant_name
        if preauthurl:
            self.os_options['object_storage_url'] = preauthurl
        self.url = preauthurl or self.os_options.get('object_storage_url')
        self.token = preauthtoken or self.os_options.get('auth_token')
        if self.os_options.get('service_username', None):
            self.service_auth = True
        else:
            self.service_auth = False
        self.service_token = None
        self.cacert = cacert
        self.insecure = insecure
        self.cert = cert
        self.cert_key = cert_key
        self.ssl_compression = ssl_compression
        self.auth_end_time = 0
        self.retry_on_ratelimit = retry_on_ratelimit
        self.timeout = timeout
        self.force_auth_retry = force_auth_retry
