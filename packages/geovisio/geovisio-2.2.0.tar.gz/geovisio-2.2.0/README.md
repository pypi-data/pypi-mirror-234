# ![GeoVisio](https://gitlab.com/geovisio/api/-/raw/develop/images/logo_full.png)

__GeoVisio__ is a complete solution for storing and __serving your own 📍📷 geolocated pictures__ (like [StreetView](https://www.google.com/streetview/) / [Mapillary](https://mapillary.com/)).

➡️ __Give it a try__ at [panoramax.ign.fr](https://panoramax.ign.fr/) or [geovisio.fr](https://geovisio.fr/viewer) !

## 📦 Components

GeoVisio is __modular__ and made of several components, each of them standardized and ♻️ replaceable.

![GeoVisio architecture](https://gitlab.com/geovisio/api/-/raw/develop/images/big_picture.png)

All of them are 📖 __open-source__ and available online:

|                               🌐 Server                                 |                      💻 Client                       |
|:-----------------------------------------------------------------------:|:----------------------------------------------------:|
|                 [API](https://gitlab.com/geovisio/api)                  |    [Website](https://gitlab.com/geovisio/website)    |
|            [Blur API](https://gitlab.com/geovisio/blurring)             | [Web viewer](https://gitlab.com/geovisio/web-viewer) |
| [GeoPic Tag Reader](https://gitlab.com/geovisio/geo-picture-tag-reader) |   [Command line](https://gitlab.com/geovisio/cli)    |


# 🌐 GeoVisio API

This repository only contains __the backend and web API__.

## Features

* A __web API__ to search and upload pictures collections
  * Search pictures by ID, date, location
  * Compatible with [SpatioTemporal Asset Catalog](https://stacspec.org/) and [OGC WFS 3](https://github.com/opengeospatial/WFS_FES) specifications
  * Upload your pictures and sequences
* An easy-to-use __backend__
  * Generates automatically thumbnail, small and tiled versions of your pictures
  * Compatible with various filesystems (classic, S3, FTP...)
  * Authentication and blurring API can be plugged-in for production-ready use


## Install & run

Our [documentation](https://gitlab.com/geovisio/api/-/tree/develop/docs) will help you install, configure and run a GeoVisio instance.

If at some point you're lost or need help, you can contact us through [issues](https://gitlab.com/geovisio/api/-/issues) or by [email](mailto:panieravide@riseup.net).


## Contributing

Pull requests are welcome. For major changes, please open an [issue](https://gitlab.com/geovisio/api/-/issues) first to discuss what you would like to change.

More information about developing is available in [documentation](https://gitlab.com/geovisio/api/-/tree/develop/docs).


## 🤗 Special thanks

![Sponsors](https://gitlab.com/geovisio/api/-/raw/develop/images/sponsors.png)

GeoVisio was made possible thanks to a group of ✨ __amazing__ people ✨ :

- __[GéoVélo](https://geovelo.fr/)__ team, for 💶 funding initial development and for 🔍 testing/improving software
- __[Carto Cité](https://cartocite.fr/)__ team (in particular Antoine Riche), for 💶 funding improvements on viewer (map browser, flat pictures support)
- __[La Fabrique des Géocommuns (IGN)](https://www.ign.fr/institut/la-fabrique-des-geocommuns-incubateur-de-communs-lign)__ for offering long-term support and funding the [Panoramax](https://panoramax.fr/) initiative and core team (Camille Salou, Mathilde Ferrey, Christian Quest, Antoine Desbordes, Jean Andreani, Adrien Pavie)
- Many _many_ __wonderful people__ who worked on various parts of GeoVisio or core dependencies we use : 🧙 Stéphane Péneau, 🎚 Albin Calais & Cyrille Giquello, 📷 [Damien Sorel](https://www.strangeplanet.fr/), Pascal Rhod, Nick Whitelegg...
- __[Adrien Pavie](https://pavie.info/)__, for ⚙️ initial development of GeoVisio
- And you all ✨ __GeoVisio users__ for making this project useful !


## ⚖️ License

Copyright (c) GeoVisio team 2022-2023, [released under MIT license](https://gitlab.com/geovisio/api/-/blob/develop/LICENSE).
