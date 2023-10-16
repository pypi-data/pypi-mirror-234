"""The Scrippy ReST API client."""
import os
import requests
from scrippy_api import ScrippyApiError, logger


class Client:
  """
  The Scrippy ReST API client.
  """

  def __init__(self, verify=True, exit_on_error=True):
    """
    Client class initialization.

    :param method
    :param: verify: Verify SSL certificate, defaults to True
    :exit_on_error: Immediately raises a ScrippyApiError in case of an error during the request, defaults to True
    """
    self.exit_on_error = exit_on_error
    self.verify = verify
    self.session = requests.Session()
    if not self.verify:
      requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

  def download(self, url, local_path, filename='', timeout=30):
    """
    Enables file download.

    :param url: The URL from which to download the file.
    :param local_path: The directory in which to save the file.
    :param filename: The local file name.
    :param timeout: The maximum wait time, defaults to 30s.
    """
    if len(filename) == 0:
      filename = url.split('/')[-1]
    filename = os.path.join(local_path, filename)
    logger.debug("[+] Downloading file")
    logger.debug(f" '-> From: {url}")
    logger.debug(f" '-> To: {filename}")
    try:
      with requests.get(url, stream=True, timeout=timeout) as response:
        response.raise_for_status()
        with open(filename, 'wb') as dl_file:
          for chunk in response.iter_content(chunk_size=8192):
            dl_file.write(chunk)
      return True
    except Exception as err:
      if self.exit_on_error:
        err_msg = f"Request error: [{err.__class__.__name__}] {err}"
        raise ScrippyApiError(err_msg) from err
      else:
        logger.warning(f"Request error: [{err.__class__.__name__}] {err}")
        return response

  def request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None, proxies=None, json=None):
    """
    Allows the execution of an HTTP request.

    :param method: The HTTP method to use.
    :param url: The URL to reach.
    :param params: The query parameters (GET) for the request, defaults to None.
    :param data: The data parameters (POST) for the request, defaults to None.
    :param headers: The headers for the request, defaults to None.
    :param cookies: The cookies for the request, defaults to None.
    :param file: The file to send (POST), defaults to None.
    :param auth: The authentication information (BASIC AUTH) as a tuple (user, password), defaults to None.
    :param timeout: The maximum wait time, defaults to None.
    :param proxies: The list of proxy servers to use, defaults to None.
    :param json: JSON to send in the request body (POST), defaults to None.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    logger.debug("[+] Sending request to server")
    default_get_kwargs = {"params": params,
                          "timeout": timeout,
                          "headers": headers,
                          "cookies": cookies,
                          "proxies": proxies,
                          "auth": auth,
                          "verify": self.verify}
    default_post_kwargs = {"data": data, "json": json, "files": files}
    # TO BE IMPLEMENTED:
    #  "CONNECT": self._connect,
    #  "OPTIONS": self._options,
    #  "TRACE": self._trace,
    #  "HEAD": self._trace,
    methods = {"GET": {"method": self._get,
                       "kwargs": default_get_kwargs},
               "POST": {"method": self._post,
                        "kwargs": {**default_get_kwargs, **default_post_kwargs}},
               "PUT": {"method": self._put,
                       "kwargs": {**default_get_kwargs, **default_post_kwargs}},
               "DELETE": {"method": self._delete,
                          "kwargs": {**default_get_kwargs, **default_post_kwargs}},
               "PATCH": {"method": self._patch,
                         "kwargs": {**default_get_kwargs, **default_post_kwargs}}}
    try:
      response = None
      response = methods[method]["method"](url, **methods[method]["kwargs"])
      response.raise_for_status()
      return response
    except Exception as err:
      if self.exit_on_error:
        err_msg = f"Request error: [{err.__class__.__name__}] {err}"
        raise ScrippyApiError(err_msg) from err
      else:
        logger.warning(f"Request error: [{err.__class__.__name__}] {err}")
        return response

  def _get(self, url, **kwargs):
    return self.session.get(url, **kwargs)

  def _post(self, url, **kwargs):
    return self.session.post(url, **kwargs)

  def _head(self, url, **kwargs):
    return self.session.head(url, **kwargs)

  def _put(self, url, **kwargs):
    return self.session.put(url, **kwargs)

  def _delete(self, url, **kwargs):
    return self.session.delete(url, **kwargs)

  def _patch(self, url, **kwargs):
    return self.session.patch(url, **kwargs)
