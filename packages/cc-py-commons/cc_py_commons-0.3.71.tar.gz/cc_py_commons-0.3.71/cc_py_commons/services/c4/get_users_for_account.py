import requests

from cc_py_commons.utils.logger import logger
from .constants import C4_API_AUTH_TOKEN, C4_API_URL


def execute(account_id, request_id=None):
  url = f"{C4_API_URL}/users/search"
  token = f"Bearer {C4_API_AUTH_TOKEN}"
  headers = {
    "Authorization": token
  }
  http_params = {
    "accountId": account_id,
    "requestId": request_id
  }

  logger.debug(f"Getting users for account: URL: {url}, Params: {http_params}")
  response = requests.get(url, params=http_params, headers=headers)

  if response.status_code != 200:
    logger.warning(f"Request to get user failed with status code: {response.status_code}")
    return None

  return response.json()
