# Picture blurring

Picture blurring can be enabled using the `API_BLUR_URL` environment variable, which should point to an API offering blurring services. The following services are compatible with GeoVisio:

- [GeoVisio blurring API](https://gitlab.com/geovisio/blurring)
- [SGBlur](https://github.com/cquest/sgblur)

GeoVisio API stores directly blurred pictures, and if blurring is enabled, doesn't keep original unblurred pictures. This ensures a good level of privacy as required by European legislation.

You can change blur API URL at anytime if you want to use another service. Pictures already blurred are not blurred again when changing provider.

## Blur API specifications

If you want to plug another blur API than the ones listed above, you have to make sure that:

- It offers a `POST /blur/` route
  - That accepts `multipart/form-data`
  - Containing a JPEG picture file under `picture` parameter
  - And returns with a `200` code the same picture, blurred, in JPEG, with all original EXIF metadata
  - Optionally, the route can have a `keep=1` URL query parameter to keep unblurred parts


## Next step

You may want to know more about [developing on the server](./19_Develop_server.md).
