from kfsd.apps.core.tests.base_api import BaseAPITestCases
from kfsd.apps.core.utils.attr import AttrUtils


class AttrUtilsTests(BaseAPITestCases):

    def test_format(self):
        data = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_merge_arr_complex_dict1.json')
        attrData = AttrUtils.format(data)
        template0 = attrData.templates[0]
        self.assertEqual(template0.identifier, "cronjob")
        template0Data0 = template0.data[0]
        self.assertEqual(template0Data0.identifier, "1")
        template0Dimensions = template0.dimensions
        self.assertEqual(template0Dimensions, ['addon:volumes', 'addon:serviceaccount'])

    def test_attr_copy(self):
        data = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_merge_arr_complex_dict1.json')
        attr0Data = AttrUtils.format(data)
        attr0template0 = attr0Data.templates[0]
        self.assertEqual(attr0template0.identifier, "cronjob")

        attr1Data = attr0Data.copy()
        attr1template0 = attr1Data.templates[0]
        self.assertEqual(attr1template0.identifier, "cronjob")
        self.assertEqual(attr0Data, attr1Data)
