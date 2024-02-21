Countries GeoJSON from https://datahub.io/core/geo-countries

Compress file by converting to lower precision, e.g. 2, and removing spaces with jq
```
python compress_geojson.py countries.geojson 2
jq -rc . countries.geojson | sponge countries.geojson
```
