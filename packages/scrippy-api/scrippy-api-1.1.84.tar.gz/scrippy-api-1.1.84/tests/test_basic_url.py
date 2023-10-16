"""Test de base du client d'API."""
import os
import pytest
from scrippy_api.api import Client
from scrippy_api import ScrippyApiError


def test_get():
  """Connection basique."""
  params = {}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  response = client.request(method="GET", url=url, params=params)
  assert response.status_code == 200


def test_bad_get():
  """Connection basique."""
  params = {"parrot": "dead"}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  with pytest.raises(ScrippyApiError) as err:
    response = client.request(method="GET", url=url, params=params)
  assert "[HTTPError] 400 Client Error: Bad Request for url: http://gunicorn:8080/user?parrot=dead" in str(err.value)


def test_get_unknown_user():
  """Connection basique."""
  params = {"first_name": "Luiggi", "last_name": "Vercotti", "password": "SP4N1SH1NQU1S1T10N"}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  with pytest.raises(ScrippyApiError) as err:
    response = client.request(method="GET", url=url, params=params)
  assert "Request error: [HTTPError] 404 Client Error: Not Found for url: http://gunicorn:8080/user?first_name=Luiggi&last_name=Vercotti&password=SP4N1SH1NQU1S1T10N" in str(err.value)


def test_download():
  """Test de téléchargement. """
  url = "https://www.mcos.nc/user/pages/01.home/_sliders/01.illustration/banner.jpg"
  local_dir = "./"
  local_path = os.path.join(local_dir, url.split('/')[-1])
  client = Client()
  assert client.download(url, local_dir)
  assert os.path.isfile(local_path)
