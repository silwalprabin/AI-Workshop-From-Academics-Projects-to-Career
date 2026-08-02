# Application configuration.
# NOTE (for the workshop): this file intentionally contains issues.

# ISSUE (security): hardcoded secret / API key committed to source control.
API_KEY = "sk_live_51H8xShDkE9zQwErTyUiOpAsDfGhJkLzXcVbNm1234567890"
DATABASE_PASSWORD = "sup3rs3cr3t_admin_password"

DEBUG = True
MAX_RETRIES = 3


def get_api_key():
    # ISSUE (docs): no docstring; returns a hardcoded secret.
    return API_KEY
