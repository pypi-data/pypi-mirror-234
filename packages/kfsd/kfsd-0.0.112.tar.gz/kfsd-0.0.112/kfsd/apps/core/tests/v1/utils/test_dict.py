from kfsd.apps.core.tests.base_api import BaseAPITestCases
from kfsd.apps.core.utils.dict import DictUtils


class DictUtilsTests(BaseAPITestCases):

    def test_dict_get_all_keys(self):
        data = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys.json')
        store_arr = []
        DictUtils.get_all_keys(store_arr, data)
        self.assertEqual(store_arr, ["bio", "first_name", "age", "address", "city", "type"])

    def test_dict_filter_by_keys_neg(self):
        data = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys.json')
        filteredDict = DictUtils.filter_by_keys_neg(data, ["bio"])
        self.assertEqual(filteredDict, {"type": "bio"})

    def test_dict_get(self):
        data = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys.json')
        typeVal = DictUtils.get(data, "type")
        self.assertEqual(typeVal, "bio")

    def test_dict_merge(self):
        dict1 = {"name": "Gokul", "bio": {"age": 41}}
        dict2 = {"type": "bio", "bio": {"address": {"city": "Bowmanville"}}}
        mergedDict = DictUtils.merge(dict1=dict1, dict2=dict2, merge_recursive=False)
        self.assertEqual(mergedDict, {"name": "Gokul", "type": "bio", "bio": {"address": {"city": "Bowmanville"}}})

        mergedDict = DictUtils.merge(dict1=dict1, dict2=dict2, merge_recursive=True)
        self.assertEqual(mergedDict, {"name": "Gokul", "type": "bio", "bio": {"age": 41, "address": {"city": "Bowmanville"}}})

    def test_dict_merge_arr(self):
        dict1 = {"arr1": [5, 1, 2, 3]}
        dict2 = {"arr1": [3, 4]}

        mergedDict1 = DictUtils.merge(dict1=dict1.copy(), dict2=dict2.copy(), merge_recursive=False)
        self.assertEqual(mergedDict1, {"arr1": [3, 4]})

        mergedDict2 = DictUtils.merge(dict1=dict1.copy(), dict2=dict2.copy(), merge_recursive=True, arr_rm_dupes=False)
        self.assertEqual(mergedDict2, {"arr1": [5, 1, 2, 3, 3, 4]})

        mergedDict3 = DictUtils.merge(dict1=dict1.copy(), dict2=dict2.copy(), merge_recursive=True, arr_rm_dupes=False, is_arr_sorted=False)
        self.assertEqual(mergedDict3, {"arr1": [5, 1, 2, 3, 3, 4]})

        mergedDict4 = DictUtils.merge(dict1=dict1.copy(), dict2=dict2.copy(), merge_recursive=True, arr_rm_dupes=False, is_arr_sorted=True)
        self.assertEqual(mergedDict4, {"arr1": [1, 2, 3, 3, 4, 5]})

        mergedDict5 = DictUtils.merge(dict1=dict1.copy(), dict2=dict2.copy(), merge_recursive=True, arr_rm_dupes=True, is_arr_sorted=True)
        self.assertEqual(mergedDict5, {"arr1": [1, 2, 3, 4, 5]})

    def test_dict_merge_arr_complex_norecursive(self):
        dict1 = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_merge_arr_complex_dict1.json')
        dict2 = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_merge_arr_complex_dict2.json')

        obsDict1 = DictUtils.merge(dict1=dict1.copy(), dict2=dict2.copy(), merge_recursive=False, is_arr_sorted=True)
        expDict1 = self.readJSONData('kfsd/apps/core/tests/v1/data/responses/utils/dict/test_dict_merge_arr_complex_norecursive.json')
        self.assertEqual(obsDict1, expDict1)

    def test_dict_merge_arr_complex_recursive_no_dupes_no_arr_sorting(self):
        dict1 = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_merge_arr_complex_dict1.json')
        dict2 = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_merge_arr_complex_dict2.json')

        obsDict2 = DictUtils.merge(dict1=dict1.copy(), dict2=dict2.copy(), merge_recursive=True, arr_rm_dupes=False, is_arr_sorted=False)
        expDict2 = self.readJSONData('kfsd/apps/core/tests/v1/data/responses/utils/dict/test_dict_merge_arr_complex_recursive_no_dupes_no_arr_sorting.json')
        self.assertEqual(obsDict2, expDict2)

    def test_dict_merge_arr_complex_recursive_dupes_arr_sorting(self):
        dict1 = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_merge_arr_complex_dict1.json')
        dict2 = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_merge_arr_complex_dict2.json')

        obsDict3 = DictUtils.merge(dict1=dict1.copy(), dict2=dict2.copy(), merge_recursive=True, arr_rm_dupes=True, is_arr_sorted=True)
        expDict3 = self.readJSONData('kfsd/apps/core/tests/v1/data/responses/utils/dict/test_dict_merge_arr_complex_recursive_dupes_arr_sorting.json')
        self.assertEqual(obsDict3, expDict3)

    def test_dict_create_hierarchy(self):
        newDict = DictUtils.create_hierarchy(["bio", "address", "city"], "Bowmanville")
        self.assertEqual(
            newDict,
            {
                "bio": {
                    "address": {
                        "city": "Bowmanville"
                    }
                }
            }
        )

    def test_key_exists(self):
        dict1 = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_merge_arr_complex_dict1.json')
        self.assertTrue(DictUtils.key_exists(dict1, "templates"))
        self.assertFalse(DictUtils.key_exists(dict1, "bio"))

    def test_get_by_path(self):
        dict1 = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys.json')
        val = DictUtils.get_by_path(dict1, "bio.address.city")
        self.assertEqual(val, "Bowmanville")

    def test_filter_by_keys(self):
        dict1 = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys.json')
        val = DictUtils.filter_by_keys(dict1, ["bio", "type"])
        self.assertEqual(dict1, val)

        val = DictUtils.filter_by_keys(dict1, ["type"])
        self.assertEqual(val, {"type": "bio"})

    def test_key_exists_multi(self):
        dict1 = self.readJSONData('kfsd/apps/core/tests/v1/data/requests/utils/dict/test_dict_get_all_keys.json')
        val = DictUtils.key_exists_multi(dict1, ["bio", "type"])
        self.assertTrue(val)

        val1 = DictUtils.key_exists_multi(dict1, ["bio", "type", "name"])
        self.assertFalse(val1)

    def test_create(self):
        dict1 = DictUtils.create(name="gokul", age=41, location="Bangalore")
        self.assertEqual(dict1, {"name": "gokul", "age": 41, "location": "Bangalore"})

    def test_sort_by_values(self):
        dict1 = {
            "key1": "abc",
            "key2": "bac",
            "key3": "cba",
        }
        val = DictUtils.sort_by_values(dict1, False)
        self.assertEqual(val, dict1)

        val1 = DictUtils.sort_by_values(dict1, True)
        self.assertEqual(val1, {"key3": "cba", "key2": "bac", "key1": "abc"})
