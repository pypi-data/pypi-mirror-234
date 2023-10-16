from rest_framework import status
from django.urls import reverse
import os

from kfsd.apps.endpoints.tests.endpoints_test_handler import EndpointsTestHandler


class ArrUtilsTestCases(EndpointsTestHandler):
    fixtures = ["v1/tests/settings.json"]

    def setUp(self):
        os.environ["env"] = "dev"
        os.environ["SETTINGS_ID"] = "SETTING=Kubefacets Production NoAuth"

        super().setUp()

    def test_utils_arr_join(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/arr/test_utils_arr_join.json"
        )
        obsResponse = self.post(reverse("utils-arr"), postData, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/responses/utils/arr/test_utils_arr_join.json"
        )
        self.assertEqual(obsResponse, expResponse)

    def test_utils_arr_intersection(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/arr/test_utils_arr_intersection.json"
        )
        obsResponse = self.post(reverse("utils-arr"), postData, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/responses/utils/arr/test_utils_arr_intersection.json"
        )
        self.assertEqual(obsResponse, expResponse)

    def test_utils_arr_merge(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/arr/test_utils_arr_merge.json"
        )
        obsResponse = self.post(reverse("utils-arr"), postData, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/responses/utils/arr/test_utils_arr_merge.json"
        )
        self.assertEqual(obsResponse, expResponse)

    def test_utils_arr_merge_uniq(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/arr/test_utils_arr_merge_uniq.json"
        )
        obsResponse = self.post(reverse("utils-arr"), postData, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/responses/utils/arr/test_utils_arr_merge_uniq.json"
        )
        self.assertEqual(obsResponse, expResponse)

    def test_utils_arr_match_and_merge(self):
        postData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/requests/utils/arr/test_utils_arr_match_and_merge.json"
        )
        obsResponse = self.post(reverse("utils-arr"), postData, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/data/responses/utils/arr/test_utils_arr_match_and_merge.json"
        )
        self.assertEqual(
            list(obsResponse["output"]["value"]), expResponse["output"]["value"]
        )
