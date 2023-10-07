import os
import shutil
import json
from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.exceptions.exec import ExecExceptionHandler

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class FileUtils:
    @staticmethod
    @ExecExceptionHandler(logger)
    def read_as_json(path):
        with open(path) as json_file:
            return json.load(json_file)

    @staticmethod
    def path_exists(destPath):
        if not os.path.exists(destPath):
            return False
        return True

    @staticmethod
    def construct_path(dir, dest):
        return os.path.join(dir, dest)

    @staticmethod
    @ExecExceptionHandler(logger)
    def copy_dir(src, dest):
        if not FileUtils.path_exists(dest):
            return shutil.copytree(src, dest)

    @staticmethod
    @ExecExceptionHandler(logger)
    def create_dir(dirPath):
        if not FileUtils.path_exists(dirPath):
            os.makedirs(dirPath)
            return True
        return False

    @staticmethod
    @ExecExceptionHandler(logger)
    def read_as_text(filePath, removeLineBreaks=True):
        fileStr = ""
        with open(filePath, "r") as file:
            fileStr = file.read()
        return fileStr.replace("\n", " ") if removeLineBreaks else fileStr

    @staticmethod
    @ExecExceptionHandler(logger)
    def read(filePath, startLineNum=0, endLineNum=None, removeLineBreaks=True):
        lines = []
        with open(filePath, "r") as file:
            lines = file.readlines()
        return (
            [x.replace("\n", "") for x in lines][startLineNum:endLineNum]
            if removeLineBreaks
            else lines[startLineNum:endLineNum]
        )

    @staticmethod
    @ExecExceptionHandler(logger)
    def write(filePath, data):
        with open(filePath, "w") as file:
            file.write(data)
            file.close()

    @staticmethod
    @ExecExceptionHandler(logger)
    def write_as_json(jsonFilePath, dictData):
        with open(jsonFilePath, "w") as jsonFile:
            json.dump(dictData, jsonFile)

    @staticmethod
    def get_dir_from_filepath(filePath):
        return os.path.dirname(filePath)

    @staticmethod
    def create_target_dir(filePath):
        destDir = FileUtils.get_dir_from_filepath(filePath)
        FileUtils.create_dir(destDir)

    @staticmethod
    @ExecExceptionHandler(logger)
    def move_file(srcFile, destFile):
        FileUtils.create_target_dir(destFile)
        shutil.move(srcFile, destFile)

    @staticmethod
    @ExecExceptionHandler(logger)
    def copy_file(srcFile, destFilePath):
        FileUtils.create_target_dir(destFilePath)
        return shutil.copy(srcFile, destFilePath)

    @staticmethod
    @ExecExceptionHandler(logger)
    def rm_dir(dirPath):
        if FileUtils.path_exists(dirPath):
            shutil.rmtree(dirPath)
            return True
        return False

    @staticmethod
    @ExecExceptionHandler(logger)
    def rm_file(filePath):
        if FileUtils.path_exists(filePath):
            os.remove(filePath)
            return True
        else:
            logger.info("Filepath: {} doesn't exist".format(filePath))
