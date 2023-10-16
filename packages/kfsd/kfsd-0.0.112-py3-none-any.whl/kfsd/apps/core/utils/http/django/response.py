from kfsd.apps.core.utils.http.django.cookie import Cookie


class DjangoResponse(Cookie):
    def __init__(self, response=None):
        self.__response = response
        Cookie.__init__(self, response)

    def getResponse(self):
        return self.__response

    def setResponse(self, response):
        self.__response = response
