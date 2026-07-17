# [Omni API](http://omni-api.hive.pt)

Simple REST API wrapper for the Omni infra-structure.

## Configuration

| Name                  | Type  | Description                                                                                                              |
| --------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------ |
| **OMNI_BASE_URL**     | `str` | The base URL that is going to be used for API connections (defaults to `http://localhost:8080/mvc/`).                    |
| **OMNI_OPEN_URL**     | `str` | The open URL for the Omni connection (defaults to `OMNI_BASE_URL`).                                                      |
| **OMNI_PREFIX**       | `str` | The default prefix to be used for API requests (defaults to `adm/`).                                                     |
| **OMNI_ID**           | `str` | The client id to be used for API connections (defaults to `None`).                                                       |
| **OMNI_SECRET**       | `str` | The secret key to be used for API connections (defaults to `None`).                                                      |
| **OMNI_REDIRECT_URL** | `str` | The URL to be used for redirection OAuth based workflow (defaults to `base,base.user,base.admin,foundation.store.list`). |
| **OMNI_USERNAME**     | `str` | The username to be used on direct workflow (defaults to `None`).                                                         |
| **OMNI_PASSWORD**     | `str` | The password to be used on direct workflow (defaults to `None`).                                                         |

## Usage

Typical usage of the Omni client implies the providing of the username and the
password inside the target omni instance (Direct Mode).

```python
api = omni.Api(
    base_url = "http://frontdoorhq.com",
    username = "YOUR_USERNAME",
    password = "YOUR_PASSWORD"
)
```

Alternatively it's possible to use the api throught an OAuth base approach using
the provided client id and secret values.

```python
api = omni.Api(
    base_url = "http://frontdoorhq.com",
    client_id = "YOUR_OAUTH_ID",
    client_secret = "YOUR_OAUTH_SECRET"
)
```

For these type of handling the `OAuthAccessError` exception must be handled and then
the user must be redirect to the url provided by `api.oauth_autorize` method call.

Running then the `api.oauth_access` call with the returned `code` from the server side
that should be used to redeem the `access_token` required for session authentication.

## Examples

Examples are located [here](src/examples).

## Testing

The unit test suite runs using [pytest](https://pytest.org) and requires Python 3.10+, unlike the library itself the tests make full use of the provided type stubs (the library implementation remains Python 2.7+ compatible).

```bash
pip install pytest
pytest
```

The live integration tests run against a local Omni instance and are skipped unless the `OMNI_TEST_LIVE` environment variable is set, together with the usual `OMNI_BASE_URL`, `OMNI_USERNAME` and `OMNI_PASSWORD` configuration.

Such an instance can be provisioned with demo data using the `hivesolutions/omni` docker image (private, registry credentials required), the loader seeds the database with the demo dataset (including the `root` / `Root@12345` credentials) and the server is then started, note that with `COLONY_PREFIX=/mvc` the client base URL should not include the `/mvc` prefix:

```bash
docker run -d --name omni -p 8080:8080 --entrypoint sh \
    -e RUN_MODE=development \
    -e COLONY_CONFIG_FILE=config/python/singleton.py \
    -e DB_ENGINE=sqlite \
    -e DB_FILE=ci.db \
    -e RESET_DB=1 \
    -e AT_TEST_MODE=1 \
    hivesolutions/omni:latest \
    -c "cd /omni && python3 scripts/load_demo_data.py && exec colony_wsgi"
OMNI_TEST_LIVE=1 OMNI_BASE_URL=http://localhost:8080/ OMNI_USERNAME=root OMNI_PASSWORD=Root@12345 pytest
```

The CI pipeline runs the same provisioning in the `Build Live` job whenever the Docker Hub credentials are available as repository secrets (`DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`), skipping the live run otherwise.

Type checking of the stubs, examples and tests is done using [Pyright](https://github.com/microsoft/pyright):

```bash
pip install pyright
pyright src/omni/*.pyi src/examples src/omni/test
```

## License

Omni API is currently licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/).

## Build Automation

[![Build Status](https://github.com/hivesolutions/omni-api/workflows/Main%20Workflow/badge.svg)](https://github.com/hivesolutions/omni-api/actions)
[![Coverage Status](https://coveralls.io/repos/hivesolutions/omni-api/badge.svg?branch=master)](https://coveralls.io/r/hivesolutions/omni-api?branch=master)
[![PyPi Status](https://img.shields.io/pypi/v/omni-api.svg)](https://pypi.python.org/pypi/omni-api)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/)
