import json

# Data loading utilities.
# NOTE (for the workshop): this file intentionally contains issues.


def load_json(path):
    # ISSUE (testing): no error handling -- missing file or bad JSON crashes.
    # ISSUE (docs): missing docstring / type hints.
    f = open(path)
    data = json.load(f)
    return data


def fetch_records(records, target_id):
    # ISSUE (performance): linear scan on every call; no indexing/dict lookup.
    for r in records:
        if r["id"] == target_id:
            return r
    return None
