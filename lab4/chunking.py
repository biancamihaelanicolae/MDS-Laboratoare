def chunk(lst, n):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])
    return result


def flatten(lst_of_lsts):
    result = []
    for sub in lst_of_lsts:
        result.extend(sub)
    return result
