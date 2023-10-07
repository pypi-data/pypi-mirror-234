import functools

from kfsd.apps.core.utils.arr import ArrUtils
from kfsd.apps.core.utils.dict import DictUtils


class Configuration:
    MASTER_KEY = "master"

    def __init__(self, **kwargs):
        self.__rawSettings = {
            tuple(item["setting"]): item
            for item in DictUtils.deepcopy(kwargs.pop("settings"))
        }
        self.__reqKeyList = [
            "{}:{}".format(k, v) for (k, v) in kwargs.pop("dimensions").items()
        ]
        self.__mergeRecursive = kwargs.get("merge_recursive", True)
        self.__arr_rm_dupes = kwargs.get("arr_rm_dupes", True)
        self.__config = self.generateConfig()

    @staticmethod
    def findConfigValues(config, paths):
        configs = [DictUtils.get_by_path(config, path) for path in paths]
        return configs

    def getFinalConfig(self):
        return self.__config

    def findSetting(self, key):
        tupleKey = tuple(key)
        return (
            {} if tupleKey not in self.__rawSettings else self.__rawSettings[tupleKey]
        )

    def getAllSubsetKeys(self, findKey):
        return [x for x in self.__rawSettings.keys() if self.isSubset(findKey, x)]

    def isSubset(self, tuple1, tuple2):
        set1 = set(tuple1)
        set2 = set(tuple2)
        if set2.issubset(set1):
            return True

        return False

    def generateConfig(self):
        childKeys = ArrUtils.sort_keys_by_len(self.getAllSubsetKeys(self.__reqKeyList))
        masterConfig = self.findSetting([self.MASTER_KEY])
        for childkey in childKeys:
            masterConfig = DictUtils.merge(
                dict1=masterConfig,
                dict2=self.findSetting(childkey),
                merge_recursive=self.__mergeRecursive,
                arr_rm_dupes=self.__arr_rm_dupes,
            )
            masterConfig.pop("setting")

        if "setting" in masterConfig:
            masterConfig.pop("setting")

        return masterConfig

    def getConfig(self, key):
        keys = key.split(".")
        value = functools.reduce(
            lambda d, key: (d.get(key) if isinstance(d, dict) else None) if d else None,
            keys,
            self.__config,
        )
        if value is None:
            raise Exception("Config key:{} not found".format(key))
        return value

    def getConfigWithDefault(self, key, default):
        try:
            return self.getConfig(key)
        except Exception:
            return default
