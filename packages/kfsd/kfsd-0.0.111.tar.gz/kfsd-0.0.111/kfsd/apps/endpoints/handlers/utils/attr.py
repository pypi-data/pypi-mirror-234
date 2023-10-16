from kfsd.apps.core.common.logger import Logger, LogLevel

from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.attr import AttrUtils
from kfsd.apps.endpoints.serializers.utils.attr import AttrUtilsOutputRespSerializer


class AttrHandler:
    OP = "op"
    EXPR = "EXPR"

    def __init__(self, input):
        self.__logger = Logger.getSingleton(__name__, LogLevel.DEBUG)
        self.__input = input

    def methodMappings(self, op):
        mapping = {
            self.EXPR: self.getAttr
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
        outputSerializer = AttrUtilsOutputRespSerializer(data=data)
        outputSerializer.is_valid()
        return outputSerializer.data

    def evaluate(self, expr, request, default=None):
        result = default
        try:
            result = eval(expr)
        except Exception as e:
            self.__logger.error("{} not found".format(e.__str__()))
        return result

    def getAttr(self):
        dictVal = DictUtils.get_by_path(self.__input, "input.dict")
        expr = DictUtils.get_by_path(self.__input, "input.expr")
        request = AttrUtils.format(dictVal)
        return self.genOutput(self.EXPR, self.evaluate(expr, request))
