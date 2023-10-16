from kfsd.apps.core.utils.http.base import HTTP
from kfsd.apps.core.utils.http.django.request import DjangoRequest
from kfsd.apps.core.utils.http.django.config import DjangoConfig
from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig


class BasePermission(HTTP):
    def __init__(self, request):
        self.__request = DjangoRequest(request)
        self.__config = DjangoConfig(KubefacetsConfig().getConfig())
        HTTP.__init__(self)

    def getDjangoRequest(self):
        return self.__request

    def getDjangoConfig(self):
        return self.__config

    def getUser(self):
        return self.getDjangoRequest().getRequest().token_user

    def getCurrentRequestUrl(self):
        return self.getDjangoRequest().getRequest().build_absolute_uri()
