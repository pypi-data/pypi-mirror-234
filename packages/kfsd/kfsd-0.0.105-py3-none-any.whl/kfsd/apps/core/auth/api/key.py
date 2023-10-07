from kfsd.apps.core.auth.api.gateway import APIGateway


class APIKeyAuth(APIGateway):
    OP_NAME = "APIKEY_USER_INFO"

    def getApiKeyUserInfo(self):
        pass
