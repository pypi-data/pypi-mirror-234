from kfsd.apps.core.tests.base_api import BaseAPITestCases
from django.urls import reverse
from unittest.mock import patch
import os


class APIDocsViewTests(BaseAPITestCases):
    fixtures = ["v1/tests/settings.json"]

    def setUp(self):
        os.environ["env"] = "auth"
        os.environ["SETTINGS_ID"] = "SETTING=Kubefacets"
        super().setUp()

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    def test_get_auth_allok(self, tokenUserInfoMocked):
        staffUserInfoResp = {
            "status": True,
            "data": {
                "user": {
                    "identifier": "123",
                    "is_staff": True,
                    "is_active": True,
                    "is_email_verified": True,
                }
            },
        }
        tokenUserInfoMocked.return_value = staffUserInfoResp
        url = reverse("api_doc")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    def test_get_auth_isnot_staff(self, tokenUserInfoMocked):
        staffUserInfoResp = {
            "status": True,
            "data": {
                "user": {
                    "identifier": "123",
                    "is_staff": False,
                    "is_active": True,
                    "is_email_verified": True,
                }
            },
        }
        tokenUserInfoMocked.return_value = staffUserInfoResp
        url = reverse("api_doc")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    def test_get_auth_isnot_active(self, tokenUserInfoMocked):
        staffUserInfoResp = {
            "status": True,
            "data": {
                "user": {
                    "identifier": "123",
                    "is_staff": True,
                    "is_active": False,
                    "is_email_verified": True,
                }
            },
        }
        tokenUserInfoMocked.return_value = staffUserInfoResp
        url = reverse("api_doc")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    def test_get_auth_isnot_emailverified(self, tokenUserInfoMocked):
        staffUserInfoResp = {
            "status": True,
            "data": {
                "user": {
                    "identifier": "123",
                    "is_staff": True,
                    "is_active": True,
                    "is_email_verified": False,
                }
            },
        }
        tokenUserInfoMocked.return_value = staffUserInfoResp
        url = reverse("api_doc")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_get_noauth(self):
        os.environ["env"] = "test"
        os.environ["SETTINGS_ID"] = "SETTING=Kubefacets"
        url = reverse("api_doc")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
