class ContentType:
    APPLICATION_JSON = "application/json"
    CONTENTTYPE_HEADER_KEY = "Content-Type"

    def __init__(self):
        self.__contentType = None

    def setContentType(self, contentType):
        self.__contentType = contentType

    def getContentType(self):
        return self.__contentType

    def hasContentType(self):
        if self.__contentType:
            return True
        return False
