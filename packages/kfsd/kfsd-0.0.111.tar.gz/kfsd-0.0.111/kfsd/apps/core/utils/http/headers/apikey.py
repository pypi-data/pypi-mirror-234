class APIKey:
    APIKEY_HEADER_KEY = "X-APIKey"

    def __init__(self):
        self.__apiKey = None

    def setAPIKey(self, apiKey):
        self.__apiKey = apiKey

    def getAPIKey(self):
        return self.__apiKey

    def hasAPIKey(self):
        if self.__apiKey:
            return True
        return False
