from kfsd.apps.core.auth.base import BaseUser
from kfsd.apps.core.auth.api.key import APIKeyAuth


class APIKeyUser(BaseUser, APIKeyAuth):
    def __init__(self, request):
        # self.setRequest(request)
        self.setUserInfo(self.getApiKeyUserInfo())
