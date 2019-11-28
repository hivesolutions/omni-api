# [Omni API](http://omni-api.hive.pt)

Simple REST API wrapper for the Omni infra-structure.

## Configuration

| Name | Type | Description |
| ----- | ----- | ----- |
| **BUDY_BASE_URL** | `str` | The base URL that is going to be used for API connections (defaults to `None`). |
| **BUDY_COUNTRY** | `str` | The country as an ISO 3166-1 to be used for API interactions (defaults to `US`). |
| **BUDY_CURRENCY** | `str` | The [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) code that describes the currency to be used for API interactions (defaults to `USD`). |
| **BUDY_USERNAME** | `str` | The username to be used for authentication (defaults to `None`). |
| **BUDY_PASSWORD** | `str` | The password to be user for authentication (defaults to `None`). |

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
