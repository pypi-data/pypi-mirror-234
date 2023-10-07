import http.cookies
from kfsd.apps.core.utils.dict import DictUtils


class Cookie:
    COOKIE_HEADER_KEY = "Cookie"

    def __init__(self, cookies={}):
        self.__httpObj = None
        self.__cookies = cookies

    def getCookiesHttpObj(self):
        return self.__httpObj

    def setCookiesHttpObj(self, httpObj):
        self.__httpObj = httpObj

    def getCookies(self):
        return self.__cookies

    def setCookies(self, cookies, collection=True):
        if not collection:
            self.__cookies = DictUtils.merge(dict1=self.__cookies, dict2=cookies)
        else:
            self.__cookies = cookies

    def hasCookies(self):
        if self.getCookies():
            return True
        return False

    def cookiesToHeaderStr(self, rmCookieKeys=[]):
        cookie_string = ""
        if self.__cookies:
            cookie = http.cookies.SimpleCookie()
            filteredCookies = DictUtils.filter_by_keys_neg(self.__cookies, rmCookieKeys)
            cookie.update(filteredCookies)
            for key, value in cookie.items():
                cookie_string += f"{key}={value}; "
            # remove the trailing '; '
            cookie_string = cookie_string[:-2]
        return cookie_string
