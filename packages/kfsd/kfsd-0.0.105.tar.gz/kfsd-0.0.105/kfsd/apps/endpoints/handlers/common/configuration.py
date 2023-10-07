from kfsd.apps.core.common.logger import Logger, LogLevel

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.configuration import Configuration
from kfsd.apps.endpoints.serializers.utils.configuration import (
    ConfigurationOutputRespSerializer,
)


class ConfigurationHandler:
    OP = "op"
    CONFIG = "CONFIG"

    def __init__(self, input):
        self.__logger = Logger.getSingleton(__name__, LogLevel.DEBUG)
        self.__input = input

    def methodMappings(self, op):
        mapping = {self.CONFIG: self.genConfig}
        return mapping[op]

    def gen(self):
        op = DictUtils.get(self.__input, self.OP)
        return self.methodMappings(op)()

    def genOutput(self, key, value):
        data = {"op": key, "output": {"value": value}}
        outputSerializer = ConfigurationOutputRespSerializer(data=data)
        outputSerializer.is_valid()
        return outputSerializer.data

    def genConfig(self):
        input = DictUtils.get(self.__input, "input", {})
        rawConfig = DictUtils.get(input, "raw_config", [])
        dimensions = DictUtils.get(input, "dimensions", {})
        recursiveMerge = DictUtils.get(input, "recursive_merge", True)
        arrRmDupes = DictUtils.get(input, "arr_rm_dupes", True)

        config = Configuration(
            settings=rawConfig,
            dimensions=dimensions,
            merge_recursive=recursiveMerge,
            arr_rm_dupes=arrRmDupes,
        )
        return self.genOutput(self.CONFIG, config.getFinalConfig())
