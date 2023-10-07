from rest_framework.test import APITestCase
from django.urls import reverse

from kfsd.apps.core.utils.file import FileUtils
from kfsd.apps.core.utils.dict import DictUtils


class BaseAPITestCases(APITestCase):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def readJSONData(self, filepath):
        return FileUtils.read_as_json(filepath)

    def readText(self, filepath, removeLineBreaks=True):
        return FileUtils.read_as_text(filepath, removeLineBreaks)

    def fetchPg(self, listUrl, currentPg):
        if currentPg:
            listUrl = listUrl + "?page={}".format(currentPg)
        return listUrl

    def detailView(self, name, identifier):
        return reverse(name, args=[identifier])

    def createView(self, name):
        return reverse(name)

    def stripCommonAttrs(self, resp):
        if isinstance(resp, dict):
            return DictUtils.filter_keys_neg(resp, ["created", "updated", "id"])
        return resp

    def stripCommonAttrsFromResults(self, resp):
        formattedResults = []
        results = DictUtils.get(resp, "results")
        if results:
            for item in results:
                strippedItem = self.stripCommonAttrs(item)
                formattedResults.append(strippedItem)

        resp["results"] = formattedResults
        return resp

    def list(self, url, currentPg, expStatus, stripCommonAttrs=True):
        paginatedUrl = self.fetchPg(url, currentPg)
        response = self.client.get(paginatedUrl, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return (
            self.stripCommonAttrsFromResults(response.data)
            if stripCommonAttrs
            else response.data
        )

    def get(self, name, identifier, expStatus, stripCommonAttrs=True):
        detailUrl = self.detailView(name, identifier)
        response = self.client.get(detailUrl, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return (
            self.stripCommonAttrs(response.data) if stripCommonAttrs else response.data
        )

    def create(self, url, data, expStatus, stripCommonAttrs=True):
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return (
            self.stripCommonAttrs(response.data) if stripCommonAttrs else response.data
        )

    def post(self, url, data, expStatus, stripCommonAttrs=True):
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return (
            self.stripCommonAttrs(response.data) if stripCommonAttrs else response.data
        )

    def patch(self, name, identifier, data, expStatus, stripCommonAttrs=True):
        detailUrl = self.detailView(name, identifier)
        response = self.client.patch(detailUrl, data=data, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return (
            self.stripCommonAttrs(response.data) if stripCommonAttrs else response.data
        )

    def delete(self, name, identifier, expStatus):
        detailUrl = self.detailView(name, identifier)
        response = self.client.delete(detailUrl, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return response
