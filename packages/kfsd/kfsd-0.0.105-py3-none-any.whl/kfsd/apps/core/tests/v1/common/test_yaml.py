from kfsd.apps.core.tests.base_api import BaseAPITestCases
from kfsd.apps.core.common.configuration import Configuration
from kfsd.apps.core.common.yaml import Yaml


class YamlTests(BaseAPITestCases):
    def test_configuration_yaml_dev(self):
        data = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/common/configuration/gateway.json')
        dimensions = {"environment": "k8s", "cluster": "mac", "type": "dev"}
        configObj = Configuration(settings=data, dimensions=dimensions, merge_recursive=True, arr_rm_dupes=True)
        obsConfig = configObj.getFinalConfig()
        yamlObj = Yaml()
        obsData = yamlObj.getYaml(yamlObj.formatDictConfig(obsConfig))
        expData = self.readText('kfsd/apps/core/tests/v1/data/responses/common/yaml/test_configuration_yaml_dev.yaml', False)
        self.assertEqual(expData, obsData)
