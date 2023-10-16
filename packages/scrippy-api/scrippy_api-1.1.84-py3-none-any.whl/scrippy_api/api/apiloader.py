"""API definition loader sub-module."""

import yaml
from scrippy_api import ScrippyApiError, logger


class ApiLoader:
  """The ApiLoader class loads API definition from a YAML file."""

  def __init__(self):
    self.api = {}

  def _walk_api(self, dic, path):
    """Load the API definition from the specified dict."""
    for key, value in dic.items():
      if isinstance(value, list):
        for action_list in value:
          for action in action_list:
            ppath = ".".join(path)
            ppath = f"{ppath}.{action}"
            path.append(ppath)
            self.api[ppath] = action_list[action]
            path.pop()
      elif isinstance(value, dict):
        path.append(key)
        self._walk_api(value, path)
        path.pop()

  def load_api(self, api_definition):
    """Load the API definition from the YAML file API definition given as argument."""
    logger.debug("[+] Loading API")
    logger.debug(f" '-> {api_definition}")
    try:
      with open(api_definition, mode="r", encoding="utf-8") as yaml_file:
        api_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
      self._walk_api(dic=api_yaml, path=[])
    except Exception as err:
      err_msg = f"Unknown error: [{err.__class__.__name__}] {err}"
      raise ScrippyApiError(err_msg) from err

  def get_endpoint_info(self, endpoint):
    """
    Returns information as a dict about specified endpoint.

    Returned value is in the {"method": <HTTP METHOD>, "url": <URL>} format.
    """
    logger.debug(f"[+] Getting data for: {endpoint}")
    try:
      return self.api[endpoint]
    except KeyError as err:
      err_msg = f"Unknown endpoint: {endpoint}"
      raise ScrippyApiError(err_msg) from err
