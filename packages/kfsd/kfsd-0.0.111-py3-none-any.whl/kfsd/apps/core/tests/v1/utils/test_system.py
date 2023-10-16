from kfsd.apps.core.tests.base_api import BaseAPITestCases
from kfsd.apps.core.utils.system import System
from kfsd.apps.core.utils.file import FileUtils


class SystemTests(BaseAPITestCases):

    def setUp(self):
        self.__systemObj = System()
        return super().setUp()

    def test_checksum(self):
        checksumStr = "My name is Nathan"
        checksum = System.checksum(checksumStr)
        self.assertEqual(checksum, 878446078)

        checksumDict = {"name": "Nathan"}
        checksum1 = System.checksum(checksumDict)
        self.assertEqual(checksum1, 915277270)

        checksumList = ["name", "nathan"]
        checksum2 = System.checksum(checksumList)
        self.assertEqual(checksum2, 882116008)

        checksumInt = 123
        checksum3 = System.checksum(checksumInt)
        self.assertEqual(checksum3, 8060929)

    def test_uuid(self):
        length = 10
        uuid = System.uuid(length)
        self.assertTrue(len(uuid) == length)

    def test_secret(self):
        length = 10
        secretCode = System.secret(length)
        self.assertTrue(len(secretCode) > length)

    def test_api_key(self):
        length = 10
        apiKey = System.api_key(length)
        self.assertTrue(len(apiKey) == length)

    def test_encrypt_key(self):
        encryptKey = self.__systemObj.encryptKey()
        self.assertTrue(self.__systemObj.getCmdExecStatus())
        self.assertTrue(len(encryptKey) > 40)

    def test_os_arch(self):
        arch = self.__systemObj.osArch()
        self.assertTrue(len(arch) > 2)

    def test_exec_cmd(self):
        cmd = "pwd"
        self.__systemObj.cmdExec(cmd, False)
        self.assertIsNone(self.__systemObj.getCmdExecOutput())

    def test_host_ip(self):
        hostIP = self.__systemObj.hostIP()
        self.assertTrue(len(hostIP) > 6)

    def test_hostname(self):
        self.assertIsNotNone(self.__systemObj.getHostName())

    def test_get_os(self):
        self.assertIsNotNone(self.__systemObj.getOS())

    def test_change_file_permission(self):
        filePath = "/tmp/utils/tmp.txt"
        writeContent = "my content"
        FileUtils.write(filePath, writeContent)

        permission = self.__systemObj.changeFilePermission("777", filePath)
        self.assertTrue(permission)
