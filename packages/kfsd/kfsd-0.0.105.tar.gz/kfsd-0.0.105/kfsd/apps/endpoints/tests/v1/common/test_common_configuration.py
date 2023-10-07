from rest_framework import status
from django.urls import reverse
import os

from kfsd.apps.endpoints.tests.endpoints_test_handler import EndpointsTestHandler


class ConfigurationTestCases(EndpointsTestHandler):
    fixtures = ["v1/tests/settings.json"]

    def setUp(self):
        os.environ["env"] = "dev"
        os.environ["SETTINGS_ID"] = "SETTING=Kubefacets Production NoAuth"
        super().setUp()

    def postYaml(
        self,
        url,
        data,
        expStatus,
    ):
        response = self.client.post(url, data, format="yaml")
        self.assertEqual(response.status_code, expStatus)
        print(response)

    def test_common_config_dev(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/common/config/test_common_config_dev.json"
        )
        obsResponse = self.post(reverse("utils-config"), postData, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/responses/common/config/test_common_config_dev.json"
        )
        self.assertEqual(obsResponse, expResponse)

    def test_common_config_prod(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/common/config/test_common_config_prod.json"
        )
        obsResponse = self.post(reverse("utils-config"), postData, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/responses/common/config/test_common_config_prod.json"
        )
        self.assertEqual(obsResponse, expResponse)
