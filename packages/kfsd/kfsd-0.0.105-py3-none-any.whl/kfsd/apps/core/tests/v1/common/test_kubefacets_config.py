import os

from kfsd.apps.core.tests.base_api import BaseAPITestCases
from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig


class KubefacetsConfigTests(BaseAPITestCases):
    fixtures = ["v1/tests/settings.json"]

    def setUp(self):
        os.environ["env"] = "dev"
        os.environ["SETTINGS_ID"] = "SETTING=Kubefacets"

    def test_kubefacets_config_local(self):
        obsConfig = KubefacetsConfig().getConfig()
        expConfig = self.readJSONData(
            "kfsd/apps/core/tests/v1/data/responses/common/kubefacets/test_kubefacets_config_local.json"
        )
        self.assertEquals(obsConfig, expConfig)

    def test_kubefacets_config_local_testenv(self):
        os.environ["env"] = "test"
        os.environ["SETTINGS_ID"] = "SETTING=Kubefacets"
        obsConfig = KubefacetsConfig().getConfig()
        expConfig = self.readJSONData(
            "kfsd/apps/core/tests/v1/data/responses/common/kubefacets/test_kubefacets_config_local_testenv.json"
        )
        self.assertEquals(obsConfig, expConfig)

    def test_kubefacets_config_remote(self):
        os.environ["SETTINGS_ID"] = "SETTING=Kubefacets Remote Setting"
        obsConfig = KubefacetsConfig().getConfig()
        expConfig = {"dimensions": {"env": "dev"}}
        self.assertEquals(obsConfig, expConfig)
