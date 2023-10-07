from collections.abc import Mapping
import functools
import copy

from kfsd.apps.core.common.logger import Logger, LogLevel

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class DictUtils:

    @staticmethod
    def deepcopy(d):
        return copy.deepcopy(d)

    @staticmethod
    def get_all_keys(arr, d):
        for k, v in d.items():
            arr.append(k)
            if isinstance(d.get(k), dict) and isinstance(v, Mapping):
                DictUtils.get_all_keys(arr, d.get(k, {}))

    @staticmethod
    def filter_by_keys_neg(dictionary: dict, visibleKeys: list) -> dict:
        return {k: v for k, v in dictionary.items() if k not in visibleKeys}

    @staticmethod
    def get(d: dict, k: str, default=None):
        if k in d:
            return d[k]
        return default

    @staticmethod
    def merge(**kwargs):
        dict1 = DictUtils.get(kwargs, "dict1", {})
        dict2 = DictUtils.get(kwargs, "dict2", {})
        merge_recursive = DictUtils.get(kwargs, "merge_recursive", True)
        arr_rm_dupes = DictUtils.get(kwargs, "arr_rm_dupes", True)
        arr_dict_lookup_key = DictUtils.get(kwargs, "arr_dict_lookupkey", "identifier")
        is_arr_sorted = DictUtils.get(kwargs, "is_arr_sorted", False)
        if not merge_recursive:
            return {**dict1, **dict2}
        return DictUtils.recursive_merge(dict1, dict2, arr_rm_dupes, arr_dict_lookup_key, is_arr_sorted)

    @staticmethod
    def recursive_merge(dict1, dict2, arr_rm_dupes=True, arr_dict_lookup_key="identifier", is_arr_sorted=True):
        for k, v in dict2.items():
            if isinstance(dict1.get(k), dict) and isinstance(v, Mapping):
                dict1[k] = DictUtils.merge(dict1=dict1.get(k, {}), dict2=v, arr_rm_dupes=arr_rm_dupes, is_arr_sorted=is_arr_sorted)
            elif isinstance(dict1.get(k), list) and isinstance(v, list):
                unionArr = dict1.get(k) + v
                dict1[k] = DictUtils.match_and_merge_arr(unionArr, arr_rm_dupes, arr_dict_lookup_key, is_arr_sorted)
            else:
                dict1[k] = v
        return dict1

    @staticmethod
    def match_and_merge_arr(arr, arr_rm_dupes=True, arr_dict_lookup_key="identifier", is_arr_sorted=True):
        isAllItemsAsDict = DictUtils.confirm_arr_items_as_dict(arr, arr_dict_lookup_key)
        if not isAllItemsAsDict or len(arr) == 0:
            arrItems = list(set(arr)) if arr_rm_dupes else arr
            return sorted(arrItems) if is_arr_sorted else arrItems

        baseDict = DictUtils.convert_arr_to_dict(arr[0], arr_dict_lookup_key)
        for item in arr[1::]:
            baseDict = DictUtils.merge(
                dict1=baseDict,
                dict2=DictUtils.convert_arr_to_dict(item, arr_dict_lookup_key),
                arr_rm_dupes=arr_rm_dupes,
                arr_dict_lookup_key=arr_dict_lookup_key,
                is_arr_sorted=is_arr_sorted
            )

        return [v for k, v in baseDict.items()]

    @staticmethod
    def convert_arr_to_dict(arr, lookupkey="identifier"):
        return {arr[lookupkey]: arr}

    @staticmethod
    def confirm_arr_items_as_dict(arr, arr_dict_lookup_key="identfier"):
        for item in arr:
            if not isinstance(item, dict) or arr_dict_lookup_key not in item:
                return False
        return True

    @staticmethod
    def create_hierarchy(keys, value):
        return functools.reduce((lambda x, y: {y: x}), keys[::-1], value)

    @staticmethod
    def key_exists(d: dict, k: str) -> bool:
        if k in d:
            return True
        return False

    @staticmethod
    def get_by_path(dictionary: dict, path: str):
        keys = path.split(".")
        return functools.reduce(lambda d, key: (d.get(key) if isinstance(d, dict) else None) if d else None, keys, dictionary)

    @staticmethod
    def filter_by_keys(dictionary: dict, visibleKeys: list) -> dict:
        return {k: v for k, v in dictionary.items() if k in visibleKeys}

    @staticmethod
    def key_exists_multi(d: dict, keys: list) -> bool:
        if all(key in d for key in keys):
            return True
        return False

    @staticmethod
    def create(**kwargs):
        return kwargs

    @staticmethod
    def sort_by_values(d, isReverse=False):
        sortedD = sorted(d.items(), key=lambda x: x[1], reverse=isReverse)
        return dict(sortedD)
