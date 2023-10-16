from kfsd.apps.core.tests.base_api import BaseAPITestCases
from kfsd.apps.core.common.configuration import Configuration


class ConfigurationTests(BaseAPITestCases):

    def test_configuration_dev(self):
        data = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/common/configuration/gateway.json')
        dimensions = {"environment": "k8s", "cluster": "mac", "type": "dev"}
        configObj = Configuration(settings=data, dimensions=dimensions, merge_recursive=True, arr_rm_dupes=True)
        obsConfig = configObj.getFinalConfig()
        expConfig = self.readJSONData('kfsd/apps/core/tests/v1/data/responses/common/configuration/test_configuration_dev.json')
        self.assertEqual(obsConfig, expConfig)

    def test_configuration_prod(self):
        data = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/common/configuration/gateway.json')
        dimensions = {"environment": "k8s", "cluster": "inhouse", "type": "prod"}
        configObj = Configuration(settings=data, dimensions=dimensions, merge_recursive=True, arr_rm_dupes=True)
        obsConfig = configObj.getFinalConfig()
        expConfig = self.readJSONData('kfsd/apps/core/tests/v1/data/responses/common/configuration/test_configuration_prod.json')
        self.assertEqual(obsConfig, expConfig)

    def test_configuration_nomerge_dev(self):
        data = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/common/configuration/gateway.json')
        dimensions = {"environment": "k8s", "cluster": "mac", "type": "dev"}
        configObj = Configuration(settings=data, dimensions=dimensions, merge_recursive=False, arr_rm_dupes=False)
        obsConfig = configObj.getFinalConfig()
        expConfig = self.readJSONData('kfsd/apps/core/tests/v1/data/responses/common/configuration/test_configuration_nomerge_dev.json')
        self.assertEqual(obsConfig, expConfig)

    def test_configuration_nomerge_prod(self):
        data = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/common/configuration/gateway.json')
        dimensions = {"environment": "k8s", "cluster": "inhouse", "type": "prod"}
        configObj = Configuration(settings=data, dimensions=dimensions, merge_recursive=False, arr_rm_dupes=False)
        obsConfig = configObj.getFinalConfig()
        expConfig = self.readJSONData('kfsd/apps/core/tests/v1/data/responses/common/configuration/test_configuration_nomerge_prod.json')
        self.assertEqual(obsConfig, expConfig)
