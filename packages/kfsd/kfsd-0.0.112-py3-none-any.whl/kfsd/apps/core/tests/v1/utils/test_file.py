from kfsd.apps.core.tests.base_api import BaseAPITestCases
from kfsd.apps.core.utils.file import FileUtils
from kfsd.apps.core.exceptions.exec import ExecException


class FileUtilsTests(BaseAPITestCases):

    def test_read_as_json(self):
        json = FileUtils.read_as_json('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys.json')
        self.assertEqual(json["type"], "bio")

    def test_read_as_json_exception(self):
        with self.assertRaises(ExecException):
            FileUtils.read_as_json('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys_tmp.json')

    def test_construct_path(self):
        filePath = FileUtils.construct_path("kfsd/apps/core/tests/v1/data/requests/utils/dict", "test_dict_get_all_keys.json")
        self.assertEqual(filePath, "kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys.json")

    def test_copy_dir(self):
        destDir = "/tmp/utils"
        FileUtils.rm_dir(destDir)
        isCreated = FileUtils.copy_dir("kfsd/apps/core/tests/v1/data/requests/utils", destDir)
        self.assertTrue(isCreated)
        self.assertTrue(FileUtils.path_exists("{}/dict".format(destDir)))
        self.assertTrue(FileUtils.path_exists("{}/dict/test_dict_get_all_keys.json".format(destDir)))

    def test_copy_dir_exception(self):
        with self.assertRaises(ExecException):
            FileUtils.copy_dir("kfsd/apps/core/tests/v1/data/requests/utils", "/var/test")

    def test_create_dir(self):
        destDir = "/tmp/utils"
        FileUtils.rm_dir(destDir)
        self.assertFalse(FileUtils.path_exists(destDir))
        isDirCreated = FileUtils.create_dir(destDir)
        self.assertTrue(isDirCreated)
        self.assertTrue(FileUtils.path_exists(destDir))
        FileUtils.rm_dir(destDir)

        dirDepthPath = destDir+"/folder1/folder2"
        isDirCreated = FileUtils.create_dir(dirDepthPath)
        self.assertTrue(isDirCreated)
        isDirCreated = FileUtils.create_dir(dirDepthPath)
        self.assertFalse(isDirCreated)
        FileUtils.rm_dir(dirDepthPath)

    def test_create_dir_exception(self):
        with self.assertRaises(ExecException):
            destDir = "/var/test/path1"
            FileUtils.create_dir(destDir)

    def test_read_as_text_rm_linebreaks(self):
        textContent = FileUtils.read_as_text('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys.json')
        self.assertTrue(type(textContent) == str)
        self.assertTrue("\n" not in textContent)
        self.assertTrue("Gokul Nathan" in textContent)

    def test_read_as_text_exception(self):
        with self.assertRaises(ExecException):
            FileUtils.read_as_text('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys_tmp.json')

    def test_read_as_text_no_rm_linebreaks(self):
        textContent = FileUtils.read_as_text('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys.json', False)
        self.assertTrue(type(textContent) == str)
        self.assertTrue("\n" in textContent)
        self.assertTrue("Gokul Nathan" in textContent)

    def test_read(self):
        textContent = FileUtils.read('kfsd/apps/core/tests/v1/data/requests/utils/file/test_read.txt')
        self.assertTrue(len(textContent) == 4)
        self.assertTrue(textContent[0] == "My name is Nathan")
        self.assertTrue("\n" not in textContent[0])

        limitedLines = FileUtils.read('kfsd/apps/core/tests/v1/data/requests/utils/file/test_read.txt', 1, 2)
        self.assertTrue(limitedLines[0] == "I live in Bowmanville")

        limitedLines1 = FileUtils.read('kfsd/apps/core/tests/v1/data/requests/utils/file/test_read.txt', 1)
        self.assertTrue(len(limitedLines1) == 3)

        limitedLines2 = FileUtils.read('kfsd/apps/core/tests/v1/data/requests/utils/file/test_read.txt', 1, 2, False)
        self.assertTrue(limitedLines2[0] == "I live in Bowmanville\n")

    def test_write_exception(self):
        with self.assertRaises(ExecException):
            FileUtils.write("/var/tmp.txt", "my content")

    def test_write(self):
        destDir = "/tmp/utils/tmp.txt"
        writeContent = "my content"
        FileUtils.rm_dir(destDir)
        FileUtils.write(destDir, writeContent)
        pathExists = FileUtils.path_exists(destDir)
        self.assertTrue(pathExists)
        readContent = FileUtils.read_as_text(destDir)
        self.assertEqual(writeContent, readContent)

    def test_write_as_json_exception(self):
        destDir = "/var/tmp.json"
        data = {"name": "Gokul"}
        with self.assertRaises(ExecException):
            FileUtils.write_as_json(destDir, data)

    def test_write_as_json(self):
        destDir = "/tmp/utils/folder1/tmp.json"
        data = {"name": "Gokul"}
        FileUtils.write_as_json(destDir, data)
        json_data = FileUtils.read_as_json(destDir)
        self.assertEqual(data, json_data)

    def test_move_file_exception(self):
        with self.assertRaises(ExecException):
            FileUtils.move_file('kfsd/apps/core/tests/v1/data/requests/utils/file/test_read.txt', '/var/test_read.txt')

    def test_move_file(self):
        destDir = "/tmp/utils/folder1/tmp.json"
        data = {"name": "Gokul"}
        FileUtils.write_as_json(destDir, data)
        FileUtils.create_dir("/tmp/utils/folder2")
        moveFilePath = "/tmp/utils/folder2/tmp.json"
        FileUtils.move_file(destDir, moveFilePath)
        pathExists = FileUtils.path_exists(moveFilePath)
        self.assertTrue(pathExists)

    def test_copy_file_exception(self):
        with self.assertRaises(ExecException):
            FileUtils.copy_file('kfsd/apps/core/tests/v1/data/requests/utils/file/test_read.txt', '/var/test_read.txt')

    def test_copy_file(self):
        copiedFile = FileUtils.copy_file('kfsd/apps/core/tests/v1/data/requests/utils/file/test_read.txt', '/tmp/utils/test_read.txt')
        self.assertTrue(copiedFile)

    def test_rm_dir_exception(self):
        with self.assertRaises(ExecException):
            FileUtils.rm_dir("/var")

    def test_rm_dir(self):
        folderPath = "/tmp/utils/folder2"
        FileUtils.create_dir(folderPath)
        self.assertTrue(FileUtils.path_exists(folderPath))

        FileUtils.rm_dir(folderPath)
        self.assertFalse(FileUtils.path_exists(folderPath))

    def test_rm_file(self):
        destFile = "/tmp/utils/folder1/tmp.json"
        data = {"name": "Gokul"}
        FileUtils.write_as_json(destFile, data)
        fileRemoved = FileUtils.rm_file(destFile)
        self.assertTrue(fileRemoved)
