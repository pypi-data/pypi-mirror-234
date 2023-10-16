import os
import requests

from cc_py_commons.utils.logger import logger

MERCURY_URL = os.environ.get("MERCURY_URL")
MERCURY_TOKEN = os.environ.get("MERCURY_TOKEN")


def execute(account_id):
    url = f"{MERCURY_URL}/account_execs"
    token = f"Bearer {MERCURY_TOKEN}"
    headers = {
        "Authorization": token
    }

    http_params = {
        "accountId": account_id,
    }

    response = requests.get(url, params=http_params, headers=headers)

    if response.status_code != 200:
        logger.warning(
            f"Lane Pricing lookup failed for params: {http_params} - {response.status_code}:{response.text}")
        return None

    return response.json()
