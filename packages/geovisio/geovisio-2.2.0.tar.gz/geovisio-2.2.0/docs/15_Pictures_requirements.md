# Organize your pictures and sequences

GeoVisio API allows both importing and serving your own pictures. Although, your pictures needs to meet some requirements to be read correctly by the API. This documentation lists requirements on pictures and sequences (serie of pictures).

## Prepare your pictures

GeoVisio has several prerequisites for a pictures to be accepted, mainly concerning availability of some [EXIF tags](https://en.wikipedia.org/wiki/Exif). A picture __must__ have the following EXIF tags defined:

- GPS coordinates with `GPSLatitude, GPSLatitudeRef, GPSLongitude, GPSLongitudeRef`
- Date, either with `GPSTimeStamp` or `DateTimeOriginal`

The following EXIF tags are recognized and used if defined, but are __optional__:

- Image orientation, either with `GPSImgDirection` or `GPano:PoseHeadingDegrees` (was mandatory in versions <= 1.3.1)
- Milliseconds in date with `SubSecTimeOriginal`
- If picture is 360° / spherical with `GPano:ProjectionType`
- Camera model with `Make, Model`
- Camera focal length (to get precise field of view) with `FocalLength`

Note that GeoVisio now accepts both __360° and classic/flat pictures__ (versions <= 1.2.0 only supported 360° pictures).

The reading of EXIF tags is done by another GeoVisio component named [GeoPic Tag Reader](https://gitlab.com/geovisio/geo-picture-tag-reader), you can check out there the source code that handles this.


## Next step

You may now want to play with the [HTTP API](./16_Using_API.md).
