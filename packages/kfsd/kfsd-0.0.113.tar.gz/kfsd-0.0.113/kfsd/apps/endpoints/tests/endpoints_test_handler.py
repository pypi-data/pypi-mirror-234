from rest_framework.test import APITestCase
from django.urls import reverse
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.utils.file import FileUtils
import os


class EndpointsTestHandler(APITestCase):
    def setUp(self):
        os.environ["env"] = "dev"
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def readJSONData(self, filepath):
        return FileUtils.read_as_json(filepath)

    def fetchPg(self, listUrl, currentPg):
        if currentPg:
            listUrl = listUrl + "?page={}".format(currentPg)
        return listUrl

    def detailView(self, name, identifier):
        return reverse(name, args=[identifier])

    def createView(self, name):
        return reverse(name)

    def rmAttrs(self, resp, stripAttrs=["created", "updated", "id"]):
        if isinstance(resp, dict):
            return DictUtils.filter_by_keys_neg(resp, stripAttrs)
        return resp

    def rmAttrsFromResults(self, resp, stripAttrs=["created", "updated", "id"]):
        formattedResults = []
        results = DictUtils.get(resp, "results")
        if results:
            for item in results:
                strippedItem = self.rmAttrs(item, stripAttrs)
                formattedResults.append(strippedItem)

        resp["results"] = formattedResults
        return resp

    def list(self, url, currentPg, expStatus, stripAttrs=["created", "updated", "id"]):
        paginatedUrl = self.fetchPg(url, currentPg)
        response = self.client.get(paginatedUrl, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return (
            self.rmAttrsFromResults(response.data, stripAttrs)
            if stripAttrs
            else response.data
        )

    def get(self, name, identifier, expStatus, stripAttrs=["created", "updated", "id"]):
        detailUrl = self.detailView(name, identifier)
        response = self.client.get(detailUrl, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return self.rmAttrs(response.data, stripAttrs) if stripAttrs else response.data

    def create(self, url, data, expStatus, stripAttrs=["created", "updated", "id"]):
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return self.rmAttrs(response.data, stripAttrs) if stripAttrs else response.data

    def post(self, url, data, expStatus, stripAttrs=["created", "updated", "id"]):
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return self.rmAttrs(response.data, stripAttrs) if stripAttrs else response.data

    def patch(
        self, name, identifier, data, expStatus, stripAttrs=["created", "updated", "id"]
    ):
        detailUrl = self.detailView(name, identifier)
        response = self.client.patch(detailUrl, data=data, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return self.rmAttrs(response.data, stripAttrs) if stripAttrs else response.data

    def delete(self, name, identifier, expStatus):
        detailUrl = self.detailView(name, identifier)
        response = self.client.delete(detailUrl, format="json")
        self.assertEqual(response.status_code, expStatus, response.data)
        return response
