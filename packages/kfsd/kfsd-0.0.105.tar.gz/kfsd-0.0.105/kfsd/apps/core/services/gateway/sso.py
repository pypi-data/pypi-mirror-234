from rest_framework import status
from kfsd.apps.core.auth.api.gateway import APIGateway
from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class SSO(APIGateway):
    def __init__(self, request=None):
        APIGateway.__init__(self, request)

    def getVerifyTokensUrl(self):
        return self.constructUrl(
            ["services.gateway_api.host", "services.gateway_api.sso.verify_tokens_uri"]
        )

    def verifyTokens(self, payload):
        return self.httpPost(self.getVerifyTokensUrl(), payload, status.HTTP_200_OK)

    def isAuthEnabled(self):
        isAuth = self.getDjangoRequest().findConfigs(
            ["services.features_enabled.auth"]
        )[0]
        return isAuth if isAuth else False
