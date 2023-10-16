![Build Status](https://drone-ext.mcos.nc/api/badges/scrippy/scrippy-api/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, my scrangourou friend](./scrippy-api.png "Scrippy, my scrangourou friend")

# `scrippy_api`

REST API client for the `Scrippy` framework (https://codeberg.org/scrippy).

## Requirements

### Python modules

#### Required modules list

The modules listed below will be automatically installed.

- requests
- PyYAML
- jsonschema

## Installation

### Manual

```bash
git clone https://codeberg.org/scrippy/scrippy-api.git
cd scrippy-api
python -m pip install -r requirements.txt
make install
```

### With `pip`

```bash
pip install scrippy-api
```

### Usage

The `scrippy_api.api` module provides the `Client` object that allows querying any [_REST API_ ](https://en.wikipedia.org/wiki/Representational_state_transfer) uniformly using the unique method `Client.request()`.

The `Client` object has a single method `Client.request()` that accepts many parameters, most of which are optional. However, some optional parameters can become mandatory depending on the HTTP method used for the request and the use case. _YMMV_.

The `Client.request()` method always returns a `requests.Response` object (see [documentation](https://2.python-requests.org/en/master/user/advanced/#request-and-response-objects)) that must be handled by the script.

Both parameter keys and values will be automatically encoded when necessary.

In case of error (HTTP code != 200), the client exits with an `1` return code and the error is logged as `critical`.
This behavior can be inhibited during the client instantiation by setting the `exit_on_error` parameter to `False`:

```python
from scrippy_api.api import Client
client = Client(exit_on_error=False)
```

In this case, any encountered errors will appear in the log file as `warning`.

The verification of the remote server SSL certificate can be disabled by passing the optional `verify` parameter of the `Client` object to `False`:

```python
from scrippy_api.api import Client
client = Client(exit_on_error=True, verify=False)
```

**Note**: Disabling certificate verification is discouraged because it presents real security risks.


#### Parameters

Parameters of the `request` method of the `Client` object:

| Parameter | Type | Description | Default value |
| --------- | ---- | ----------- | ------------- |
| `params`  | Dictionary | Applicable to all HTTP methods. Each key/value pair will be concatenated to the URL. | `None` |
| `cookies` | Dictionary | Cookies to be sent with the request | `None` |
| `timeout` | integer | Waiting time before interrupting the connection | `None` |
| `headers` | Dictionary | Headers to be sent with the request | `None` |
| `proxies` | List | List of proxy servers to use for the connection | `None` |
| `auth`    | Tuple | Username and password for _BASIC AUTH_ authentication |
| `data`    | Dictionary | Data to be sent with the request. Not applicable with `GET` method | `None` |
| `json`    | Dictionary | Data in _JSON_ format to be sent with the request. Not applicable with `GET` method. Use when `data` and `file` are not specified | `None` |
| `files`   | Dictionary | Files to be uploaded in _multipart_. The dictionary takes the form `{<file name>: <file>}`  | `None` |


Implemented HTTP methods:

| HTTP method | Description |
| -----------| ------------ |
| `GET`        | Retrieve a resource or list of resource URIs |
| `POST`       | Create a resource |
| `PUT`        | Replace or create a resource |
| `PATCH`      | Update a resource or create it if non-existent |
| `DELETE`     | Delete a resource |



#### Examples

##### URL with Parameters

```python
from scrippy_api.api import Client
params = {"name": "Luiggi Vercotti", "password": "dead/parrot"}
client = Client()
response = client.request(method="GET", url="https://montypython.org/user", params=params)
```

The called URL will be:
```
https://montypython.org/user?name=Luiggi+Vercotti&password=dead%2Fparrot
```

##### Basic Authentication (BASIC AUTH)

Basic authentication with the following credentials:
- Username: `Luiggi Vercotti`
- Password: `dead/parrot`

```python
from scrippy_api.api import Client
auth = ("Luiggi Vercotti", "dead/parrot")
client = Client()
response = client.request(method="POST", url="https://montypython.org", auth=auth)
```

##### Sending Data

Creating the `Luiggi Vercotti` user with the password `dead/parrot`:

```python
from scrippy_api.api import Client
data = {"name": "Luiggi Vercotti", "password": "dead/parrot"}
client = Client()
response = client.request(method="POST", url="https://montypython.org/user", data=data)
```

##### File Upload

Upload of the two files `./images/dead_parrot.png` and `./images/flying_circus.mp4`:

```python
from scrippy_api.api import Client
files = {"dead_parrot.png": open("./images/dead_parrot.png", "rb"), "flying_circus.mp4": open("./images/flying_circus.mp4", "rb")}
client = Client()
response = client.request(method="POST", url="https://montypython.org/upload", data=data)
```

##### Resource Modification

Replaces the password of the `Luiggi Vercotti` user

```python
from scrippy_api.api import Client
auth = ("Luiggi Vercotti", "dead/parrot")
data = {"password": "live/parrot"}
params = {"name": "Luiggi Vercotti"}
client = Client()
response = client.request(method="PATCH",
                          url="https://montypython.org/user",
                          params=params,
                          data=data)
```

##### File Download

```python
from scrippy_api.api import Client
url = "https://monthy.python/inquisition.zip"
local_dir = "/home/luiggi.vercotti"
local_filename = "spanish_inquisition.zip"
client = Client()
if client.download(url, local_dir, local_filename):
  print("No one expects the Spanish inquisition")
```
