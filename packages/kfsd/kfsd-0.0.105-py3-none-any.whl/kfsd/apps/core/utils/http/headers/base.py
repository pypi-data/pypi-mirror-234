from kfsd.apps.core.utils.http.headers.cookie import Cookie
from kfsd.apps.core.utils.http.headers.contenttype import ContentType
from kfsd.apps.core.utils.http.headers.apikey import APIKey
from kfsd.apps.core.utils.http.headers.csrf import CSRF


class Headers(Cookie, ContentType, APIKey, CSRF):
    def __init__(self):
        Cookie.__init__(self)
        ContentType.__init__(self)
        APIKey.__init__(self)
        CSRF.__init__(self)
        self.__headers = {}

    def getReqHeaders(self):
        if self.hasCookies():
            self.__headers[self.COOKIE_HEADER_KEY] = self.cookiesToHeaderStr()

        if self.hasContentType():
            self.__headers[self.CONTENTTYPE_HEADER_KEY] = self.getContentType()

        if self.hasAPIKey():
            self.__headers[self.APIKEY_HEADER_KEY] = self.getAPIKey()

        if self.hasCSRF():
            self.__headers[self.CSRF_HEADER_KEY] = self.getCSRF()

        return self.__headers
