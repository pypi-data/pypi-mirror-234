class CSRF:
    CSRF_HEADER_KEY = "X-CSRFToken"

    def __init__(self):
        self.__csrf = None

    def setCSRF(self, csrf):
        self.__csrf = csrf

    def getCSRF(self):
        return self.__csrf

    def hasCSRF(self):
        if self.__csrf:
            return True
        return False
