# Using the HTTP API

By default, your Geovisio HTTP API is available on [localhost:5000](http://localhost:5000/).

The HTTP API allows you to access to collections (sequences), items (pictures) and their metadata. Geovisio API is following the [STAC API specification](https://github.com/radiantearth/stac-api-spec/blob/main/overview.md), which is based on OGC API and a widely-used standard for geospatial imagery. More info about STAC [is available online](https://stacspec.org/en).

API routes are documented at [localhost:5000/api/docs/swagger](http://localhost:5000/api/docs/swagger) ([online version](https://panoramax.ign.fr/api/docs/swagger)). Note that [OpenAPI specification is also available](http://localhost:5000/api/docs/specs.json) ([online version](https://panoramax.ign.fr/api/docs/specs.json)).


## Authentication

If activated at the GeoVisio's instance level, some routes might need authentication.

### OAuth flow

The main way to authenticate on the API is based on [OAuth 2.0](https://wikipedia.org/wiki/OAuth).

The authentication is asked to the configured instance's OAuth provider and stored in a session cookie.

The routes that need authentication should redirect to the `/api/auth/login` route if no session cookie is set.

A logout from the instance can be done via the `/api/auth/logout` route.

### Bearer token

Protected routes can also be accessed with a [JWT](https://wikipedia.org/wiki/JSON_Web_Token) [Bearer token](https://datatracker.ietf.org/doc/html/rfc6750).

Those tokens are needed when using the API without a browser, for example when doing regular [curl](https://curl.se/) calls or with our __[command-line client](https://gitlab.com/geovisio/cli)__.

The JWT token should be given to the API via the `Authorization` header as a bearer token.

For example in curl it is done like (considering your GeoVisio server is `https://geovisio.fr/`):

```bash
curl https://geovisio.fr/api/users/me --header "Authorization: Bearer <A_JWT_TOKEN>"
```

And with [httpie](https://httpie.io) (at least httpie 3.0.0 is needed):

```bash
http -A bearer -a <A_JWT_TOKEN> https://geovisio.fr/api/users/me
```

#### How to get a token

##### Via an OAuth logged call

To get a JWT token, a regular user need to user a browser and call `/api/users/me/tokens`.

This will trigger an OAuth dance, and if the OAuth provider validates the user's credentials, this will return a list of geovisio tokens like:

```json
[
  {
    "description": "default token",
    "generated_at": "2023-05-11T15:56:59.410095+00:00",
    "id": "e11c255c-6023-4eee-bb47-31566f4ce65f",
    "links": [
      {
        "href": "https://geovisio.fr/api/users/me/tokens/e11c255c-6023-4eee-bb47-31566f4ce65f",
        "rel": "self",
        "type": "application/json"
      }
    ]
  }
]
```

A geovisio token can be converted to a JWT token by calling (also in a browser, since an authenticated session cookie is needed):

`api/users/me/tokens/:id` with the ID of a token.

This will return a json with a `jwt_token` field which is the token needed as Bearer token.

An example result would be:
```json
{
  "description": "default token",
  "generated_at": "2023-05-11T15:56:59.410095+00:00",
  "id": "e11c255c-6023-4eee-bb47-31566f4ce65f",
  "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnZW92aXNpbyIsInN1YiI6ImUxMWMyNTVjLTYwMjMtNGVlZS1iYjQ3LTMxNTY2ZjRjZTY1ZiJ9.vGJz-AgFgP4T5pZqGVK49-HcZXvOeFZm3EEIYrAJ44M"
}
```

With this example, accessing a protected route with this jwt token could be done with:

```bash
curl https://geovisio.fr/api/users/me --header "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnZW92aXNpbyIsInN1YiI6ImUxMWMyNTVjLTYwMjMtNGVlZS1iYjQ3LTMxNTY2ZjRjZTY1ZiJ9.vGJz-AgFgP4T5pZqGVK49-HcZXvOeFZm3EEIYrAJ44M"
```

##### Via pregenerated token

Tokens can be fearsome, but GeoVisio support a nicer way to generate them.

A token not associated to any account can be generated with a POST on `/api/auth/tokens/generate`:

```bash
curl -X POST https://geovisio.fr/api/auth/tokens/generate
```

This will return a new token, with its JWT counterpart like:

```json
{
  "description": "",
  "generated_at": "2023-05-23T15:58:26.645393+00:00",
  "id": "ee649235-bf10-4b04-a09a-64b1663af6f8",
  "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnZW92aXNpbyIsInN1YiI6ImVlNjQ5MjM1LWJmMTAtNGIwNC1hMDlhLTY0YjE2NjNhZjZmOCJ9.MoZYN9gsqiCQL3GrN2k6fZ21msrxFFtAZSEA3ClkKc0",
  "links": [
    {
      "href": "https://geovisio.fr/api/auth/tokens/ee649235-bf10-4b04-a09a-64b1663af6f8/claim",
      "rel": "claim",
      "type": "application/json"
    }
  ]
}
```

This JWT token can be saved somewhere, but will not be usable until an account is associated with it.

An account can be associated with it by opening in a browser the `claim` url in the `links` section. (the url `https://geovisio.fr/api/auth/tokens/ee649235-bf10-4b04-a09a-64b1663af6f8/claim` in the example below).

Opening the URL will trigger an OAuth dance in the browser, and if the user is successfully logged in, the token will be associated to its account.

[GeoVisio CLI](https://gitlab.com/geovisio/cli) uses this mechanism to hide token complexity to the users.

##### JWT token for the instance administrator

An instance administrator can get the JWT token of the default instance's account with the flask command `default-account-token get`

```bash
❯ flask default-account-token get
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnZW92aXNpbyIsInN1YiI6ImUxMWMyNTVjLTYwMjMtNGVlZS1iYjQ3LTMxNTY2ZjRjZTY1ZiJ9.vGJz-AgFgP4T5pZqGVK49-HcZXvOeFZm3EEIYrAJ44M
```

This token can then be used to authenticate api calls as bearer token. This is especially useful when running an instance without an OAuth provider.

The instance need to be configurated with a valid `FLASK_SECRET_KEY` for this to work (cf [instance configuration](./11_Server_settings.md#flask-parameters)).

Note: Be sure not to share this token!

#### Revoking a token

A token can be revoked (definitely deleted) by calling a `DELETE` on `/api/users/me/tokens/<uuid:token_id>`

This calls needs to be logged, another token (or even the same one) can be used.

```bash
❯ curl -XDELETE https://geovisio.fr/api/users/me/tokens/ee649235-bf10-4b04-a09a-64b1663af6f8 --header "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnZW92aXNpbyIsInN1YiI6ImVlNjQ5MjM1LWJmMTAtNGIwNC1hMDlhLTY0YjE2NjN
hZjZmOCJ9.MoZYN9gsqiCQL3GrN2k6fZ21msrxFFtAZSEA3ClkKc0"
{
  "message": "token revoked"
}
```

## Upload

GeoVisio also offers API routes to upload pictures and sequences. Simplest way to upload pictures is by using our __[command-line client](https://gitlab.com/geovisio/cli)__.

You can also use a third-party tool to work directly with HTTP requests. Upload should go through different steps:

1. Create a new sequence with `POST /api/collections`. It will give you back a sequence ID that you will need for next steps.
2. Upload as many pictures as wanted with `POST /api/collections/<SEQUENCE ID>/items`. Both a JPEG image file and a numeric position in sequence are needed.
3. Wait a bit for server to process (save, read metadata and blur) your pictures. You can check status using `GET /api/collections/<SEQUENCE ID>/geovisio_status` to see the progress made on process.
4. Enjoy your brand-new uploaded sequence with `GET /api/collections/<SEQUENCE ID>/items` !

You can go through these steps with the following _cURL_ bash commands (considering your GeoVisio server is `https://geovisio.fr/`):

```bash
# Create collection
# You will have in both Location HTTP response header
# and in JSON response body the sequence ID
curl \
	-i -d "title=My%20sequence" \
	https://geovisio.fr/api/collections

# We consider below sequence ID is 60d94628-8098-42cc-b684-ffb9aa9d35a7

# Send a first picture
# You will have in both Location HTTP response header
# and in JSON response body the picture ID
curl \
	-i -F "picture=@my_picture_001.jpg" \
	-F "position=1" \
	-F "isBlurred=false" \ # Optional, you can set this to "true" to skip blurring
	https://geovisio.fr/api/collections/60d94628-8098-42cc-b684-ffb9aa9d35a7/items

# Send as many pictures as you want...
# Just mind changing the position parameter

# Check processing status
# If all items are ready, you're good to go !
curl https://geovisio.fr/api/collections/60d94628-8098-42cc-b684-ffb9aa9d35a7/geovisio_status

# Get whole sequence as GeoJSON
curl https://geovisio.fr/api/collections/60d94628-8098-42cc-b684-ffb9aa9d35a7/items
```

## Next steps

At this point, you might either be interested in:

- [Learn more about blur API](./17_Blur_API.md)
- [Make developments on the server](./19_Develop_server.md)
- [Start using our web viewer](https://gitlab.com/geovisio/web-viewer)
