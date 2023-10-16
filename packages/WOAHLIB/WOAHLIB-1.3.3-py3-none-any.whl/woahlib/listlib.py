def merge_lists(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    missing_in_list1 = set2 - set1
    missing_in_list2 = set1 - set2

    merged_list = list1 + list(missing_in_list1) + list(missing_in_list2)

    return merged_list

