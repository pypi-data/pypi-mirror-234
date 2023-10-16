from geovisio.web import utils

API_CONFIG = {
    "openapi": "3.0.2",
    "paths": {
        "/api/docs/specs.json": {
            "get": {
                "summary": "The OpenAPI 3 specification for this API",
                "tags": ["Metadata"],
                "responses": {
                    "200": {
                        "description": "JSON file documenting API routes",
                        "content": {"application/json": {"schema": {"$ref": "https://spec.openapis.org/oas/3.0/schema/2021-09-28"}}},
                    }
                },
            }
        },
        "/api/docs/swagger": {
            "get": {
                "summary": "The human-readable API documentation",
                "tags": ["Metadata"],
                "responses": {"200": {"description": "API Swagger", "content": {"text/html": {}}}},
            }
        },
    },
    "components": {
        "securitySchemes": {
            "bearerToken": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
            "cookieAuth": {"type": "apiKey", "in": "cookie", "name": "session"},
        },
        "schemas": {
            "STACLanding": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/core/openapi.yaml#/components/schemas/landingPage"},
            "STACConformance": {"$ref": "http://schemas.opengis.net/ogcapi/features/part1/1.0/openapi/schemas/confClasses.yaml"},
            "STACCatalog": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/core/openapi.yaml#/components/schemas/catalog"},
            "STACCollections": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/collections/openapi.yaml#/components/schemas/collections"
            },
            "STACCollection": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/collections/openapi.yaml#/components/schemas/collection"
            },
            "STACCollectionItems": {
                # The following link is the one that should be used, but is broken due to geometryCollectionGeoJSON definition
                # "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/featureCollectionGeoJSON"
                # So using instead copy/pasta version
                "type": "object",
                "required": ["type", "features"],
                "properties": {
                    "type": {"type": "string", "enum": ["FeatureCollection"]},
                    "features": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/STACItem"},
                    },
                    "links": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/links"
                    },
                    "timeStamp": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/timeStamp"
                    },
                    "numberMatched": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/numberMatched"
                    },
                    "numberReturned": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/numberReturned"
                    },
                },
            },
            "STACItem": {
                # The following link is the one that should be used, but is broken due to geometryCollectionGeoJSON definition
                # "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/item"
                # So using instead copy/pasta version
                "type": "object",
                "description": "A GeoJSON Feature augmented with foreign members that contain values relevant to a STAC entity",
                "required": ["stac_version", "id", "type", "geometry", "bbox", "links", "properties", "assets"],
                "properties": {
                    "type": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/itemType"
                    },
                    "geometry": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/pointGeoJSON"
                    },
                    "properties": {"type": "object", "nullable": "true"},
                    "stac_version": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/stac_version"
                    },
                    "stac_extensions": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/stac_extensions"
                    },
                    "id": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/itemId"
                    },
                    "links": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/links"
                    },
                    "properties": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/properties"
                    },
                    "assets": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/ogcapi-features/openapi.yaml#/components/schemas/assets"
                    },
                },
            },
            "STACExtent": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/collections/openapi.yaml#/components/schemas/extent"},
            "STACExtentTemporal": {
                "type": "object",
                "properties": {
                    "temporal": {
                        "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/collections/openapi.yaml#/components/schemas/extent/properties/temporal"
                    },
                },
            },
            "STACStatsForItems": {"$ref": "https://stac-extensions.github.io/stats/v0.2.0/schema.json#/definitions/stats_for_items"},
            "STACLinks": {
                "type": "object",
                "properties": {
                    "links": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/collections/openapi.yaml#/components/schemas/links"}
                },
            },
            "STACItemSearchBody": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/schemas/searchBody"
            },
            "GeoVisioLanding": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACLanding"},
                    {"type": "object", "properties": {"extent": {"$ref": "#/components/schemas/STACExtent"}}},
                ]
            },
            "GeoVisioCatalog": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCatalog"},
                    {
                        "type": "object",
                        "properties": {
                            "links": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["href", "rel"],
                                    "properties": {
                                        "stats:items": {"$ref": "#/components/schemas/STACStatsForItems"},
                                        "extent": {"$ref": "#/components/schemas/STACExtentTemporal"},
                                        "geovisio:status": {"$ref": "#/components/schemas/GeoVisioCollectionStatus"},
                                    },
                                },
                            }
                        },
                    },
                ]
            },
            "GeoVisioCollectionOfCollection": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollection"},
                    {
                        "type": "object",
                        "properties": {
                            "links": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["href", "rel"],
                                    "properties": {
                                        "stats:items": {"$ref": "#/components/schemas/STACStatsForItems"},
                                        "extent": {"$ref": "#/components/schemas/STACExtentTemporal"},
                                        "geovisio:status": {"$ref": "#/components/schemas/GeoVisioCollectionStatus"},
                                        "created": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "Upload date of the collection",
                                        },
                                        "updated": {
                                            "type": "string",
                                            "format": "date-time",
                                            "description": "Update date of the collection",
                                        },
                                    },
                                },
                            }
                        },
                    },
                ]
            },
            "GeoVisioCollections": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollections"},
                    {"$ref": "#/components/schemas/STACLinks"},
                    {
                        "type": "object",
                        "properties": {"collections": {"type": "array", "items": {"$ref": "#/components/schemas/GeoVisioCollection"}}},
                    },
                ]
            },
            "GeoVisioCollectionsRSS": {
                "type": "object",
                "xml": {"name": "rss"},
                "required": ["version", "channel"],
                "properties": {
                    "version": {"type": "string", "example": "2.0", "xml": {"attribute": True}},
                    "channel": {
                        "type": "object",
                        "required": ["title", "link", "description", "generator", "docs"],
                        "properties": {
                            "title": {"type": "string"},
                            "link": {"type": "string", "format": "uri"},
                            "description": {"type": "string"},
                            "language": {"type": "string"},
                            "lastBuildDate": {"type": "string"},
                            "generator": {"type": "string"},
                            "docs": {"type": "string", "format": "uri"},
                            "image": {
                                "type": "object",
                                "properties": {
                                    "url": {"type": "string", "format": "uri"},
                                    "title": {"type": "string"},
                                    "link": {"type": "string", "format": "uri"},
                                },
                            },
                            "item": {"type": "array", "items": {"$ref": "#/components/schemas/GeoVisioItemRSS"}},
                        },
                    },
                },
            },
            "GeoVisioCollection": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollection"},
                    {"type": "object", "properties": {"stats:items": {"$ref": "#/components/schemas/STACStatsForItems"}}},
                ]
            },
            "GeoVisioCollectionImportStatus": {
                "type": "object",
                "properties": {
                    "status": {"$ref": "#/components/schemas/GeoVisioCollectionStatus"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "status": {"$ref": "#/components/schemas/GeoVisioItemStatus"},
                                "rank": {"type": "integer"},
                            },
                        },
                    },
                },
            },
            "GeoVisioPostCollection": {
                "type": "object",
                "properties": {"title": {"type": "string", "description": "The sequence title"}},
            },
            "GeoVisioPatchCollection": {
                "type": "object",
                "properties": {
                    "visible": {
                        "type": "string",
                        "description": "Should the sequence be publicly visible ?",
                        "enum": ["true", "false", "null"],
                        "default": "null",
                    }
                },
            },
            "GeoVisioCollectionItems": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACCollectionItems"},
                    {"$ref": "#/components/schemas/STACLinks"},
                    {
                        "type": "object",
                        "properties": {"features": {"type": "array", "items": {"$ref": "#/components/schemas/GeoVisioItem"}}},
                    },
                ]
            },
            "GeoVisioItem": {
                "allOf": [
                    {"$ref": "#/components/schemas/STACItem"},
                    {
                        "type": "object",
                        "properties": {
                            "properties": {
                                "type": "object",
                                "properties": {
                                    "geovisio:status": {"$ref": "#/components/schemas/GeoVisioItemStatus"},
                                    "geovisio:producer": {"type": "string"},
                                    "geovisio:image": {"type": "string", "format": "uri"},
                                    "geovisio:thumbnail": {"type": "string", "format": "uri"},
                                },
                            }
                        },
                    },
                ],
            },
            "GeoVisioItemRSS": {
                "type": "object",
                "required": ["title", "link", "description", "author", "pubDate", "point"],
                "properties": {
                    "title": {"type": "string"},
                    "link": {"type": "string", "format": "uri"},
                    "description": {"type": "string"},
                    "author": {"type": "string"},
                    "pubDate": {"type": "string"},
                    "enclosure": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string", "format": "uri", "xml": {"attribute": True}},
                            "length": {"type": "integer", "xml": {"attribute": True}},
                            "type": {"type": "string", "xml": {"attribute": True}},
                        },
                    },
                    "guid": {"type": "string", "format": "uri"},
                    "point": {"type": "string", "xml": {"namespace": "http://www.georss.org/georss", "prefix": "georss"}},
                    "encoded": {"type": "string", "xml": {"namespace": "http://purl.org/rss/1.0/modules/content/", "prefix": "content"}},
                },
            },
            "GeoVisioPostItem": {
                "type": "object",
                "properties": {
                    "position": {"type": "integer", "description": "Position of picture in sequence (starting from 1)"},
                    "picture": {
                        "type": "string",
                        "format": "binary",
                        "description": "Picture to upload",
                    },
                    "isBlurred": {
                        "type": "string",
                        "description": "Is picture blurred",
                        "enum": ["true", "false", "null"],
                        "default": "false",
                    },
                    "override_capture_time": {
                        "type": "string",
                        "format": "date-time",
                        "description": "datetime when the picture was taken. It will change the picture's metadata with this datetime. It should be an iso 3339 formated datetime (like '2017-07-21T17:32:28Z')",
                    },
                    "override_latitude": {
                        "type": "number",
                        "format": "double",
                        "description": "latitude of the picture in decimal degrees (WGS84 / EPSG:4326). It will change the picture's metadata with this latitude.",
                    },
                    "override_longitude": {
                        "type": "number",
                        "format": "double",
                        "description": "longitude of the picture in decimal degrees (WGS84 / EPSG:4326). It will change the picture's metadata with this longitude.",
                    },
                },
            },
            "GeoVisioPatchItem": {
                "type": "object",
                "properties": {
                    "visible": {
                        "type": "string",
                        "description": "Should the picture be publicly visible ?",
                        "enum": ["true", "false", "null"],
                        "default": "null",
                    }
                },
            },
            "GeoVisioCollectionStatus": {"type": "string", "enum": ["ready", "broken", "preparing", "waiting-for-process"]},
            "GeoVisioItemStatus": {
                "type": "string",
                "enum": ["ready", "broken", "preparing", "waiting-for-process", "preparing-derivates", "preparing-blur"],
            },
            "GeoVisioUser": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "format": "uuid"},
                    "name": {"type": "string"},
                    "links": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {"href": {"type": "string"}, "ref": {"type": "string"}, "type": {"type": "string"}},
                        },
                    },
                },
            },
            "GeoVisioUserAuth": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "format": "uuid"},
                    "name": {"type": "string"},
                    "oauth_provider": {"type": "string"},
                    "oauth_id": {"type": "string"},
                },
            },
            "GeoVisioConfiguration": {
                "type": "object",
                "properties": {
                    "auth": {
                        "type": "object",
                        "properties": {
                            "user_profile": {"type": "object", "properties": {"url": {"type": "string"}}},
                            "enabled": {"type": "boolean"},
                        },
                        "required": ["enabled"],
                    },
                    "license": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "SPDX id of the license"},
                            "url": {"type": "string"},
                        },
                        "required": ["id"],
                    },
                },
                "required": ["auth"],
            },
            "GeoVisioTokens": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "description": {"type": "string"},
                        "generated_at": {"type": "string"},
                        "links": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {"href": {"type": "string"}, "ref": {"type": "string"}, "type": {"type": "string"}},
                            },
                        },
                    },
                },
            },
            "JWToken": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "description": {"type": "string"},
                    "generated_at": {"type": "string"},
                    "jwt_token": {
                        "type": "string",
                        "description": "this jwt_token will be needed to authenticate future queries as Bearer token",
                    },
                },
            },
            "JWTokenClaimable": {
                "allOf": [
                    {"$ref": "#/components/schemas/JWToken"},
                    {
                        "type": "object",
                        "properties": {
                            "links": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "href": {"type": "string"},
                                        "ref": {"type": "string"},
                                        "type": {"type": "string"},
                                    },
                                },
                            }
                        },
                    },
                ]
            },
        },
        "parameters": {
            "STAC_bbox": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/bbox"},
            "STAC_intersects": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/intersects"
            },
            "STAC_datetime": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/datetime"
            },
            "STAC_limit": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/limit"},
            "STAC_ids": {"$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/ids"},
            "STAC_collectionsArray": {
                "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/parameters/collectionsArray"
            },
        },
        "responses": {
            "STAC_search": {
                "description": "the items list",
                "content": {
                    "application/geo+json": {
                        "schema": {
                            "$ref": f"https://api.stacspec.org/v{utils.STAC_VERSION}/item-search/openapi.yaml#/components/schemas/itemCollection"
                        }
                    }
                },
            },
        },
    },
    "specs": [
        {
            "endpoint": "swagger",
            "route": "/api/docs/specs.json",
        }
    ],
    "swagger_ui": True,
    "specs_route": "/api/docs/swagger",
}


def getApiDocs(apiMeta: object):
    """Returns API documentation object for Swagger"""

    return {
        "info": {
            "title": apiMeta["name"],
            "version": apiMeta["version"],
            "description": apiMeta["description"],
            "contact": {"name": apiMeta["maintainer"], "url": apiMeta["url"], "email": apiMeta["maintainer_email"]},
        },
        "tags": [
            {"name": "Metadata", "description": "API metadata"},
            {"name": "Sequences", "description": "Collections of pictures"},
            {"name": "Pictures", "description": "Geolocated images"},
            {"name": "Map", "description": "Tiles for web map display"},
            {"name": "Upload", "description": "Sending pictures & sequences"},
            {"name": "Editing", "description": "Modifying pictures & sequences"},
            {"name": "Users", "description": "Account management"},
            {"name": "Auth", "description": "User authentication"},
        ],
    }
