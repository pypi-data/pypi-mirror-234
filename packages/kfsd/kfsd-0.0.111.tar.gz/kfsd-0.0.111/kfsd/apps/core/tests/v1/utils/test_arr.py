from kfsd.apps.core.tests.base_api import BaseAPITestCases
from kfsd.apps.core.utils.arr import ArrUtils


class ArrUtilsTests(BaseAPITestCases):

    def test_intersection(self):
        arr1 = [1, 2, 3, 7, 7]
        arr2 = [4, 7, 8, 2, 7]

        self.assertEqual(ArrUtils.intersection(arr1, arr2), [2, 7])

        self.assertEqual(ArrUtils.intersection([0, 6], [7, 8]), [])

    def test_merge(self):
        arr1 = [1, 2, 3, 7, 7]
        arr2 = [4, 7, 8, 2, 7]
        mergedArr = ArrUtils.merge(arr1, arr2, False)

        self.assertEqual(mergedArr, [1, 2, 2, 3, 4, 7, 7, 7, 7, 8])

        mergedArrUniq = ArrUtils.merge(arr1, arr2, True)

        self.assertEqual(mergedArrUniq, [1, 2, 3, 4, 7, 8])

    def test_join(self):
        arr1 = [1, 2, 3, 7, 7]
        joinedStr = ArrUtils.join(arr1, "|")

        self.assertEqual(joinedStr, "1|2|3|7|7")

    def test_sort_keys_by_len(self):
        keys = [
            ["env:k8s", "cluster:k8s", "type:dev"],
            ["env:k8s"],
            ["master"],
            ["cluster:inhouse", "type:dev"]
        ]

        sortedKeys = ArrUtils.sort_keys_by_len(keys)

        expKeys = [['env:k8s'], ['master'], ['cluster:inhouse', 'type:dev'], ['env:k8s', 'cluster:k8s', 'type:dev']]
        self.assertEqual(sortedKeys, expKeys)

        sortedKeysRev = ArrUtils.sort_keys_by_len(keys, True)
        expKeysRev = [['env:k8s', 'cluster:k8s', 'type:dev'], ['cluster:inhouse', 'type:dev'], ['env:k8s'], ['master']]
        self.assertEqual(sortedKeysRev, expKeysRev)

    def test_to_dict(self):
        arr1 = [
            {
                "id": 1,
                "name": "Gokul",
                "Gender": "M"
            },
            {
                "id": 2,
                "name": "Lavanya",
                "Gender": "F"
            }
        ]

        expDict = {
            1: {
                "id": 1,
                "name": "Gokul",
                "Gender": "M"
            },
            2: {
                "id": 2,
                "name": "Lavanya",
                "Gender": "F"
            }
        }

        obsDict = ArrUtils.to_dict(arr1, "id")
        self.assertEqual(obsDict, expDict)
