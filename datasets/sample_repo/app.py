from analytics import average, find_common_users
from config import get_api_key
from data_loader import load_json

# Tiny entry point tying the sample modules together.
# NOTE (for the workshop): this file intentionally contains issues.


def run():
    # ISSUE (docs): no docstring.
    # ISSUE (security): prints a secret to stdout / logs.
    print("Using API key:", get_api_key())

    users_a = ["alice", "bob", "carol"]
    users_b = ["bob", "carol", "dave"]
    print("Common users:", find_common_users(users_a, users_b))

    # ISSUE (testing): passes an empty list -> unhandled ZeroDivisionError.
    print("Average:", average([]))

    config = load_json("settings.json")
    print("Loaded config:", config)


if __name__ == "__main__":
    run()
