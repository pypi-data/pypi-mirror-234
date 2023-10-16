from kfsd.apps.core.utils.dict import DictUtils


class BaseUser:
    is_active = False

    def __init__(self):
        self.__userInfo = {}

    def setUserInfo(self, userInfo):
        self.__userInfo = userInfo

    def getUserInfo(self):
        return self.__userInfo

    def isAuthenticated(self):
        return DictUtils.get(self.getUserInfo(), "status", False)

    def getIdentifier(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.identifier")

    def getAPIKey(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.api_key")

    def isActive(self):
        return DictUtils.get_by_path(self.getUserInfo(), "data.user.is_active")
