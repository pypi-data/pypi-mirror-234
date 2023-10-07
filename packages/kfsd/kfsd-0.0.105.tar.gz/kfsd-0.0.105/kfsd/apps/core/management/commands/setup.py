from django.core.management.base import BaseCommand

from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.file import FileUtils
from kfsd.apps.core.utils.system import System

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class Command(BaseCommand):
    help = "Dev setup"

    def add_arguments(self, parser):
        parser.add_argument(
            "-c",
            "--config",
            type=str,
            help="Settings",
        )
        parser.add_argument(
            "-d",
            "--working_dir",
            type=str,
            help="Working Dir",
        )
        parser.add_argument(
            "-u",
            "--utils",
            type=str,
            help="Is Utils Pkg",
        )
        parser.add_argument(
            "-mm",
            "--makemigration",
            type=bool,
            default=True,
            help="Make Migrations",
        )
        parser.add_argument(
            "-m",
            "--migrate",
            type=bool,
            default=True,
            help="Make Migrations",
        )

    def genPyEnv(self, utilsVersion):
        FileUtils.rm_file("db.sqlite3")
        if utilsVersion:
            self.updateUtilsPkg(utilsVersion)

    def makeMigrations(self, settingsPath, workingDir, utilsVersion):
        system = System()
        if utilsVersion:
            migrationsDir = FileUtils.construct_path(
                workingDir, "kubefacets/apps/backend/migrations"
            )
            FileUtils.rm_dir(migrationsDir)
            FileUtils.create_dir(migrationsDir)

            kfsdMigrationsDir = FileUtils.construct_path(
                workingDir,
                "py_env/lib/python3.10/site-packages/kfsd/apps/models/migrations",
            )
            FileUtils.rm_dir(kfsdMigrationsDir)
            FileUtils.create_dir(kfsdMigrationsDir)
            cmds = [
                "touch {}/__init__.py".format(migrationsDir),
                "touch {}/__init__.py".format(kfsdMigrationsDir),
            ]
            system.cmdsExec(cmds, False)
        else:
            migrationsDir = FileUtils.construct_path(
                workingDir, "kfsd/apps/models/migrations"
            )
            FileUtils.rm_dir(migrationsDir)
            FileUtils.create_dir(migrationsDir)
            cmd = "touch {}/__init__.py".format(migrationsDir)
            system.cmdExec(cmd, False)

        cmds = ["python manage.py makemigrations --settings={}".format(settingsPath)]
        system.cmdsExec(cmds, False)

    def migrate(self, settingsPath):
        system = System()
        cmds = ["python manage.py migrate --settings={}".format(settingsPath)]
        system.cmdsExec(cmds, False)

    def updateUtilsPkg(self, utilsVersion):
        filePath = "requirements.txt"
        requirements = FileUtils.read(filePath)
        requirements = [req for req in requirements if not req.startswith("kfsd")]
        requirements.append("kfsd=={}".format(utilsVersion))
        requirementsStr = "\n".join(requirements)
        FileUtils.write(filePath, requirementsStr)

    def devSetup(
        self, settingsPath, workingDir, utilsVersion, isMakeMigrations, isMigrate
    ):
        self.genPyEnv(utilsVersion)
        if isMakeMigrations:
            self.makeMigrations(settingsPath, workingDir, utilsVersion)
        if isMigrate:
            self.migrate(settingsPath)

    def handle(self, *args, **options):
        logger.info("Dev Setup...")
        workingDir = DictUtils.get(options, "working_dir")
        utilsVersion = DictUtils.get(options, "utils", None)
        isMakeMigrations = DictUtils.get(options, "makemigration")
        isMigrate = DictUtils.get(options, "migrate")
        settingsPath = DictUtils.get(options, "config")
        logger.info(
            "Recd settings_path: {}, working_dir: {}, is_utils_pkg: {}, is_make_migrations: {}, is_migrate: {}".format(
                settingsPath, workingDir, utilsVersion, isMakeMigrations, isMigrate
            )
        )
        self.devSetup(
            settingsPath, workingDir, utilsVersion, isMakeMigrations, isMigrate
        )
