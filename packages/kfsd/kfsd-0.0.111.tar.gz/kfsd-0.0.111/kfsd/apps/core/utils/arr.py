from kfsd.apps.core.utils.dict import DictUtils


class ArrUtils:

    # items that are common between both arrays
    @staticmethod
    def intersection(arr1, arr2):
        return list((set(arr1) & set(arr2)))

    # merge 2 lists
    @staticmethod
    def merge(arr1, arr2, arr_rm_dupes=True, arr_dict_lookup_key="identifier", is_arr_sorted=True):
        mergedArr = arr1 + arr2
        return DictUtils.match_and_merge_arr(mergedArr, arr_rm_dupes, arr_dict_lookup_key, is_arr_sorted)

    # join array using join_str
    @staticmethod
    def join(arr, join_str):
        return join_str.join(map(str, arr))

    @staticmethod
    def sort_keys_by_len(keys, isReverse=False):
        return sorted(keys, key=len, reverse=isReverse)

    @staticmethod
    def to_dict(arr, key):
        return {item[key]: item for item in arr}
