from kfsd.apps.core.common.logger import Logger, LogLevel

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.arr import ArrUtils
from kfsd.apps.endpoints.serializers.utils.arr import ArrUtilsOutputRespSerializer


class ArrHandler:
    OP = "op"
    JOIN = "JOIN"
    INTERSECTION = "INTERSECTION"
    MERGE = "MERGE"

    def __init__(self, input):
        self.__logger = Logger.getSingleton(__name__, LogLevel.DEBUG)
        self.__input = input

    def methodMappings(self, op):
        mapping = {
            self.JOIN: self.join,
            self.INTERSECTION: self.intersection,
            self.MERGE: self.merge,
        }
        return mapping[op]

    def gen(self):
        op = DictUtils.get(self.__input, self.OP)
        return self.methodMappings(op)()

    def genOutput(self, key, value):
        data = {
            "op": key,
            "output": {
                "value": value
            }
        }
        outputSerializer = ArrUtilsOutputRespSerializer(data=data)
        outputSerializer.is_valid()
        return outputSerializer.data

    def join(self):
        arr = DictUtils.get_by_path(self.__input, "input.arr")
        join_str = DictUtils.get_by_path(self.__input, "input.str")
        return self.genOutput(self.JOIN, ArrUtils.join(arr, join_str))

    def intersection(self):
        arr1 = DictUtils.get_by_path(self.__input, "input.arr1")
        arr2 = DictUtils.get_by_path(self.__input, "input.arr2")
        return self.genOutput(self.INTERSECTION, ArrUtils.intersection(arr1, arr2))

    def merge(self):
        arr1 = DictUtils.get_by_path(self.__input, "input.arr1")
        arr2 = DictUtils.get_by_path(self.__input, "input.arr2")
        is_uniq = DictUtils.get_by_path(self.__input, "input.is_uniq")
        arr_lookup_key = DictUtils.get_by_path(self.__input, "input.lookup_key")
        return self.genOutput(self.MERGE, ArrUtils.merge(arr1, arr2, is_uniq, arr_lookup_key if arr_lookup_key else "identifier"))
