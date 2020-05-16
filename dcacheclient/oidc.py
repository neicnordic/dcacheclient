import requests
import liboidcagent as oidc

class OidcAuth(requests.auth.AuthBase):
    """Support for authenticating with OIDC access token"""
    def __init__(self, account):
        self.account = account

    def __call__(self, r):
        token = oidc.get_access_token(self.account)
        r.headers.update({'Authorization': "Bearer {}".format(token)})
        return r
