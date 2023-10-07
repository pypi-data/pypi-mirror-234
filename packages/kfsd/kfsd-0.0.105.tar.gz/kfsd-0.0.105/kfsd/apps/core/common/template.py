import re
import functools


class Template:
    def __init__(
        self, template, context, globalVars, failOnPathNotFound=False, defaultAttrs={}
    ):
        self.__template = template
        self.__context = context
        self.__vars = globalVars
        self.__failOnPathNotFound = failOnPathNotFound
        self.__defaultAttrs = defaultAttrs
        self.__prevStrVal = ""

    def mergeValues(self):
        return self.mergeValuesByType(self.__template)

    def get(self, key, context, isDefaultContext=False):
        keys = key.split(".")
        value = functools.reduce(
            lambda d, key: (d.get(key) if isinstance(d, dict) else None) if d else None,
            keys,
            context,
        )
        # Don't do validations, just send the value if found or None
        if isDefaultContext:
            return value

        # If not defaultContext , then try to get value from defaultContext first
        if value is None:
            value = self.get(key, self.__defaultAttrs, True)

        if value is None:
            if self.__failOnPathNotFound:
                raise Exception("key:{} not found in context".format(key))
            else:
                return "{{ " + key + " }}"
        return value

    def mergeValuesByType(self, rawValue):
        if type(rawValue) == dict:
            return self.mergeMapValues(rawValue)
        elif type(rawValue) == list:
            return self.mergeListValues(rawValue)
        elif type(rawValue) == str:
            return self.mergeStrValue(rawValue)

        return rawValue

    def mergeMapValues(self, mapValues):
        return {
            key: self.mergeValuesByType(rawValue) for key, rawValue in mapValues.items()
        }

    def mergeListValues(self, listValues):
        return [self.mergeValuesByType(listItem) for listItem in listValues]

    def getVariableStrMatch(self, stringValue):
        return self.getVariableStrPattern().findall(stringValue)

    def getVariableStrPattern(self):
        return re.compile(r"(\{\{(.*?)\}\})+")

    def findContext(self, key):
        return self.get(key, self.__context) if self.__context else "{{ " + key + " }}"

    def replaceAllGlobalVariables(self, stringValue):
        if self.__vars:
            for k, v in self.__vars.items():
                stringValue = (
                    stringValue.replace(k, v)
                    if len(self.getVariableStrMatch(v)) == 0
                    else v
                )
        return stringValue

    def mergeStrValue(self, stringValue):
        if (
            self.__prevStrVal
            and self.__prevStrVal == stringValue
            and not self.__failOnPathNotFound
        ):
            return stringValue
        stringValue = self.replaceAllGlobalVariables(stringValue)
        matchedList = self.getVariableStrMatch(stringValue)
        self.__prevStrVal = stringValue
        if len(matchedList) == 0:
            return stringValue

        newStringVal = stringValue
        if len(matchedList) == 1:
            item = matchedList[0]
            newStringVal = self.mergeValuesByType(self.findContext(item[1].strip()))
            newStringVal = (
                newStringVal
                if not isinstance(newStringVal, str)
                else self.getVariableStrPattern().sub(newStringVal, stringValue)
            )
        if len(matchedList) > 1:
            for item in matchedList:
                subtituteVal = self.mergeValuesByType(self.findContext(item[1].strip()))
                newStringVal = newStringVal.replace(item[0], str(subtituteVal))
        return newStringVal
