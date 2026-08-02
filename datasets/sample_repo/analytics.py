# Analytics helpers.
# NOTE (for the workshop): this file intentionally contains issues.


def find_common_users(list_a, list_b):
    # ISSUE (performance): O(n*m) nested loop; could use set intersection.
    # ISSUE (docs): missing docstring and type hints.
    common = []
    for a in list_a:
        for b in list_b:
            if a == b:
                common.append(a)
    return common


def average(numbers):
    # ISSUE (testing): no error handling for an empty list -> ZeroDivisionError.
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)


def count_duplicates(items):
    # ISSUE (performance): repeatedly scans the whole list inside the loop.
    duplicates = 0
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j]:
                duplicates += 1
    return duplicates
