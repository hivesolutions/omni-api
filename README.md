# [Omni API](http://omni-api.hive.pt)

Simple REST API wrapper for the Omni infra-structure.

## Configuration

| Name | Type | Description |
| ----- | ----- | ----- |
| **OMNI_BASE_URL** | `str` | The base URL that is going to be used for API connections (defaults to `http://localhost:8080/mvc/`). |
| **OMNI_OPEN_URL** | `str` | The open URL for the Omni connection (defaults to `OMNI_BASE_URL`). |
| **OMNI_PREFIX** | `str` | The default prefix to be used for API requests (defaults to `adm/`). |
| **OMNI_ID** | `str` | The client id to be used for API connections (defaults to `None`). |
| **OMNI_SECRET** | `str` | The secret key to be used for API connections (defaults to `None`). |
| **OMNI_REDIRECT_URL** | `str` | The URL to be used for redirection OAuth based workflow (defaults to `base,base.user,base.admin,foundation.store.list`). |
| **OMNI_USERNAME** | `str` | The username to be used on direct workflow (defaults to `None`). |
| **OMNI_PASSWORD** | `str` | The password to be used on direct workflow (defaults to `None`). |

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
