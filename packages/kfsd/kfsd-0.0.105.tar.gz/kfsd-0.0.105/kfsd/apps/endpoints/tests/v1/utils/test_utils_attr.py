from rest_framework import status
from django.urls import reverse
import os

from kfsd.apps.endpoints.tests.endpoints_test_handler import EndpointsTestHandler


class AttrUtilsTestCases(EndpointsTestHandler):
    fixtures = ["v1/tests/settings.json"]

    def setUp(self):
        os.environ["env"] = "dev"
        os.environ["SETTINGS_ID"] = "SETTING=Kubefacets Production NoAuth"
        super().setUp()

    def test_utils_expr(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/attr/test_utils_expr.json"
        )
        obsResponse = self.post(reverse("utils-attr"), postData, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/responses/utils/attr/test_utils_expr.json"
        )
        self.assertEqual(obsResponse, expResponse)
