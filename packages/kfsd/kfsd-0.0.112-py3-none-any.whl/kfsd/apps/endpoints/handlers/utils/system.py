from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.endpoints.serializers.utils.system import SystemOutputRespSerializer
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.system import System


class SystemHandler:
    OP = "op"
    INPUT = "input"
    CHECKSUM = "CHECKSUM"
    UUID = "UUID"
    SECRET = "SECRET"
    KEY = "KEY"
    ENCRYPT_KEY = "ENCRYPT_KEY"
    OS_ARCH = "OS_ARCH"
    HOST_IP = "HOST_IP"
    NIC = "NIC"
    HOSTNAME = "HOSTNAME"
    OS = "OS"

    def __init__(self, input):
        self.__logger = Logger.getSingleton(__name__, LogLevel.DEBUG)
        self.__input = input
        self.__system = System()

    def methodMappings(self, op):
        mapping = {
            self.CHECKSUM: self.genChecksum,
            self.UUID: self.genUUID,
            self.SECRET: self.genSecret,
            self.KEY: self.genKey,
            self.ENCRYPT_KEY: self.encryptKey,
            self.OS_ARCH: self.osArch,
            self.HOST_IP: self.hostIP,
            self.NIC: self.getNIC,
            self.HOSTNAME: self.getHostName,
            self.OS: self.getOS
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
        outputSerializer = SystemOutputRespSerializer(data=data)
        outputSerializer.is_valid()
        return outputSerializer.data

    def genChecksum(self):
        data = DictUtils.get_by_path(self.__input, "input.data")
        return self.genOutput(self.CHECKSUM, System.checksum(data))

    def genUUID(self):
        len = DictUtils.get_by_path(self.__input, "input.len")
        return self.genOutput(self.CHECKSUM, System.uuid(len))

    def genSecret(self):
        len = DictUtils.get_by_path(self.__input, "input.len")
        return self.genOutput(self.CHECKSUM, System.secret(len))

    def genKey(self):
        len = DictUtils.get_by_path(self.__input, "input.len")
        return self.genOutput(self.CHECKSUM, System.api_key(len))

    def encryptKey(self):
        key = DictUtils.get_by_path(self.__input, "input.key")
        return self.genOutput(self.ENCRYPT_KEY, self.__system.encryptKey(key))

    def osArch(self):
        return self.genOutput(self.OS_ARCH, self.__system.osArch())

    def hostIP(self):
        return self.genOutput(self.HOST_IP, self.__system.hostIP())

    def getNIC(self):
        return self.genOutput(self.NIC, self.__system.getNIC())

    def getHostName(self):
        return self.genOutput(self.HOSTNAME, self.__system.getHostName())

    def getOS(self):
        return self.genOutput(self.OS, self.__system.getOS())
