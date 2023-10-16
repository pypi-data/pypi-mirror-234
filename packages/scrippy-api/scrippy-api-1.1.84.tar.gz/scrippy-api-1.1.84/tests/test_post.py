"""Test POST/PUT/PATCH/DELETE du client d'API."""
import json
import pytest
from scrippy_api.api import Client
from scrippy_api import ScrippyApiError


def test_post():
  """POST."""
  data = {"user": {"first_name": "Harry", "last_name": "Fink", "password": "D3ADP4RR0T"}}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  response = client.request(method="POST", url=url, data=json.dumps(data))
  assert response.status_code == 200


def test_bad_post():
  """POST."""
  data = {"user": {"parrot": "dead"}}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  with pytest.raises(ScrippyApiError) as err:
    response = client.request(method="POST", url=url, data=json.dumps(data))
  assert "[HTTPError] 400 Client Error: Bad Request for url: http://gunicorn:8080/user" in str(err.value)


def test_put():
  """PUT."""
  data = {"user": {"first_name": "Harry", "last_name": "Fink", "password": "D3ADP4RR0T"}}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  response = client.request(method="PUT", url=url, data=json.dumps(data))
  assert response.status_code == 200


def test_bad_put():
  """PUT."""
  data = {"user": {"parrot": "dead"}}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  with pytest.raises(ScrippyApiError) as err:
    response = client.request(method="PUT", url=url, data=json.dumps(data))
  assert "[HTTPError] 400 Client Error: Bad Request for url: http://gunicorn:8080/user" in str(err.value)


def test_patch():
  """PATCH."""
  data = {"user": {"first_name": "Harry", "last_name": "Fink", "password": "D3ADP4RR0T"}}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  response = client.request(method="PATCH", url=url, data=json.dumps(data))
  assert response.status_code == 200


def test_bad_patch():
  """PUT."""
  data = {"user": {"parrot": "dead"}}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  with pytest.raises(ScrippyApiError) as err:
    response = client.request(method="PATCH", url=url, data=json.dumps(data))
  assert "[HTTPError] 400 Client Error: Bad Request for url: http://gunicorn:8080/user" in str(err.value)


def test_delete():
  """DELETE."""
  data = {"user": {"first_name": "Harry", "last_name": "Fink", "password": "D3ADP4RR0T"}}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  response = client.request(method="DELETE", url=url, data=json.dumps(data))
  assert response.status_code == 200


def test_bad_delete():
  """PUT."""
  data = {"user": {"parrot": "dead"}}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  with pytest.raises(ScrippyApiError) as err:
    response = client.request(method="DELETE", url=url, data=json.dumps(data))
  assert "[HTTPError] 400 Client Error: Bad Request for url: http://gunicorn:8080/user" in str(err.value)


def test_delete_unknown_user():
  """PUT."""
  data = {"user": {"first_name": "Luiggi", "last_name": "Vercotti", "password": "SP4N1SH1NQU1S1T10N"}}
  url = "http://gunicorn:8080/user"
  client = Client(verify=False)
  with pytest.raises(ScrippyApiError) as err:
    response = client.request(method="DELETE", url=url, data=json.dumps(data))
  assert "Request error: [HTTPError] 404 Client Error: Not Found for url: http://gunicorn:8080/user" in str(err.value)
