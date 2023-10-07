from rest_framework import status
from django.urls import reverse
import os

from kfsd.apps.endpoints.tests.endpoints_test_handler import EndpointsTestHandler
from kfsd.apps.core.utils.dict import DictUtils


class SystemUtilsTestCases(EndpointsTestHandler):
    fixtures = ["v1/tests/settings.json"]

    def setUp(self):
        os.environ["env"] = "dev"
        os.environ["SETTINGS_ID"] = "SETTING=Kubefacets Production NoAuth"
        super().setUp()

    def get(self, url, expStatus, stripCommonAttrs=True):
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return (
            self.stripCommonAttrs(response.data) if stripCommonAttrs else response.data
        )

    def test_utils_system_checksum_str(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/system/test_utils_system_checksum_str.json"
        )
        obsResponse = self.post(reverse("utils-system"), postData, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/responses/utils/system/test_utils_system_checksum_str.json"
        )
        self.assertEqual(obsResponse, expResponse)

    def test_utils_system_checksum_dict(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/system/test_utils_system_checksum_dict.json"
        )
        obsResponse = self.post(reverse("utils-system"), postData, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/responses/utils/system/test_utils_system_checksum_dict.json"
        )
        self.assertEqual(obsResponse, expResponse)

    def test_utils_system_uuid(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/system/test_utils_system_uuid.json"
        )
        obsResponse = self.post(reverse("utils-system"), postData, status.HTTP_200_OK)
        uuid = DictUtils.get_by_path(obsResponse, "output.value")
        self.assertTrue(len(uuid) == 32)

    def test_utils_system_secret(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/system/test_utils_system_secret.json"
        )
        obsResponse = self.post(reverse("utils-system"), postData, status.HTTP_200_OK)
        secret = DictUtils.get_by_path(obsResponse, "output.value")
        self.assertTrue(len(secret) > 32)

    def test_utils_system_key(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/system/test_utils_system_key.json"
        )
        obsResponse = self.post(reverse("utils-system"), postData, status.HTTP_200_OK)
        key = DictUtils.get_by_path(obsResponse, "output.value")
        self.assertTrue(len(key) == 10)
