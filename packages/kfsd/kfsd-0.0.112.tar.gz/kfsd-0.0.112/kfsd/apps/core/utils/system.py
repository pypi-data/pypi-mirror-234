import zlib
import json
import secrets
import binascii
import time
import subprocess
import shlex
import netifaces
import socket
import os
import base64

from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.exceptions.exec import ExecExceptionHandler
from kfsd.apps.core.utils.file import FileUtils

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class System:
    def __init__(self, **kwargs):
        self.__cmdExecStatus = False
        self.__cmdExecOutput = None

    def setCmdExecStatus(self, cmdStatus):
        self.__cmdExecStatus = cmdStatus

    def getCmdExecStatus(self):
        return self.__cmdExecStatus

    def setCmdExecOutput(self, cmdOutput):
        self.__cmdExecOutput = cmdOutput

    def getCmdExecOutput(self):
        return self.__cmdExecOutput

    def encryptKey(self, key=None):
        if not key:
            self.cmdExec("head -c 32 /dev/urandom | base64")
        else:
            self.cmdExec("echo {} | base64".format(key))
        return self.getCmdExecOutput()

    def osArch(self):
        self.cmdExec("uname -m")
        return self.getCmdExecOutput().lower()

    def hostIP(self):
        return netifaces.ifaddresses(self.getNIC())[netifaces.AF_INET][0]["addr"]

    def getNIC(self):
        nicPath = "/sys/class/net/{}/"
        if FileUtils.path_exists(nicPath.format("eth0")):
            return "eth0"
        elif FileUtils.path_exists(nicPath.format("enp5s0")):
            return "enp5s0"
        return "en0"

    def getHostName(self):
        return socket.gethostname()

    def getOS(self):
        self.cmdExec("uname")
        return self.getCmdExecOutput()

    def changeFilePermission(self, permission, filePath):
        self.cmdExec("chmod {} {}".format(permission, filePath))
        return self.getCmdExecStatus()

    def cmdsExec(self, cmds, captureOutput=True, shell=False):
        return [
            self.cmdExec(cmd, captureOutput, shell)
            if not type(cmd) == list
            else self.cmdsExec(cmd, captureOutput, shell)
            for cmd in cmds
        ]

    def cmdExec(self, cmd, captureOutput=True, shell=False):
        if captureOutput:
            cmdOutput = subprocess.getstatusoutput(cmd)
            cmdExecStatus = True if cmdOutput[0] == 0 else False
            cmdOutput = cmdOutput[1]
            self.setCmdExecStatus(cmdExecStatus)
            self.setCmdExecOutput(cmdOutput)
        else:
            logger.info("CMD: {}".format(cmd))
            proc = subprocess.Popen(
                shlex.split(cmd) if not shell else cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=shell,
                universal_newlines=True,
            )
            for line in iter(proc.stdout.readline, ""):
                logger.debug("{}".format(line.strip()))
            proc.stdout.close()

    @staticmethod
    @ExecExceptionHandler(logger)
    def sleep(seconds):
        time.sleep(seconds)

    @staticmethod
    def getEnv(envKey):
        return os.getenv(envKey)

    @staticmethod
    @ExecExceptionHandler(logger)
    def checksum(data):
        formattedData = None
        if isinstance(data, str):
            formattedData = data.encode("utf-8")
        elif isinstance(data, list) or isinstance(data, dict):
            formattedData = json.dumps(data).encode("utf-8")
        else:
            formattedData = bytes(data)

        return zlib.adler32(formattedData) & 0xFFFFFFFF

    @staticmethod
    @ExecExceptionHandler(logger)
    def uuid(len):
        return secrets.token_hex(int(len / 2))

    @staticmethod
    @ExecExceptionHandler(logger)
    def secret(len):
        return secrets.token_urlsafe(len)

    @staticmethod
    @ExecExceptionHandler(logger)
    def api_key(len):
        api_key_bytes = secrets.token_bytes(int(len / 2))
        return binascii.hexlify(api_key_bytes).decode("utf-8")

    @staticmethod
    def base64Encode(content, encode="utf-8"):
        encoded_bytes = base64.b64encode(content.encode(encode))
        return encoded_bytes.decode(encode)

    @staticmethod
    def base64Decode(content, decode="utf-8"):
        return base64.b64decode(content).decode(decode)
