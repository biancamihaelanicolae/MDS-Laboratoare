def merge_intervals(intervals):
    if not intervals:
        return []
    sorted_ivs = sorted(intervals, key=lambda x: x[0])
    result = [sorted_ivs[0]]
    for start, end in sorted_ivs[1:]:
        prev_start, prev_end = result[-1]
        if start <= prev_end + 1:
            result[-1] = (prev_start, max(prev_end, end))
        else:
            result.append((start, end))
    return result
