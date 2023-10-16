
def get_all_sub_sets_from_start(array) -> list:
    return [array[:i] for i in range(1, len(array) + 1)]

def concat_list_and_deduplicate(l1 : list, l2 : list) -> list:
    return list(set(l1 + l2))