import http.cookies

from kfsd.apps.core.utils.dict import DictUtils


class Cookie:
    KEY = 'key'
    COOKIE = 'cookie'
    EXPIRY_IN_SECS = 'expiry_in_secs'
    SECURE = 'secure'
    HTTP_ONLY = 'http_only'
    SAME_SITE = 'same_site'

    def __init__(self, httpObj):
        self.__httpObj = httpObj

    def getHttpObj(self):
        return self.__httpObj

    def setHttpObj(self, httpObj):
        self.__httpObj = httpObj

    def getAllCookies(self):
        return self.__httpObj.COOKIES

    def getCookie(self, key):
        return self.__httpObj.COOKIES.get(key)

    def setCookie(self, **kwargs):
        self.getHttpObj().set_cookie(
                key=kwargs[self.KEY],
                value=kwargs[self.COOKIE],
                expires=kwargs[self.EXPIRY_IN_SECS],
                secure=kwargs[self.SECURE],
                httponly=kwargs[self.HTTP_ONLY],
                samesite=kwargs[self.SAME_SITE]
            )

    def cookiesToHeaderStr(self, rmCookieKeys=[]):
        cookie_string = ''
        if self.getAllCookies():
            cookie = http.cookies.SimpleCookie()
            filteredCookies = DictUtils.filter_by_keys_neg(self.getAllCookies(), rmCookieKeys)
            cookie.update(filteredCookies)
            for key, value in cookie.items():
                cookie_string += f'{key}={value}; '
            # remove the trailing '; '
            cookie_string = cookie_string[:-2]
        return cookie_string
