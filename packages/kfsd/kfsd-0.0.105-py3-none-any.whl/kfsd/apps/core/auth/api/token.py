from kfsd.apps.core.services.gateway.sso import SSO
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class TokenAuth(SSO):
    def __init__(self, request=None):
        SSO.__init__(self, request)

    def getTokenUserInfo(self):
        payload = {
            "cookies": self.getDjangoRequest().getDjangoReqCookies().getAllCookies()
        }
        return self.verifyTokens(payload)
