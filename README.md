# projects-manager

### Description:

API to manage _“projects”._

_“Project”_ in our terminology is a plot of land, that we will be analyzing by utilizing the
satellite imagery captured in selected date range.


### Questions:

Questions I should have asked. (but I did not, shame on me 😓)

1. How 'area of interest' is going to be send: POST file upload or POST request body?
2. Should the API support additional GeoJSON types like FeatureCollection or only Feature with MultiPolygon geometry?
3. Should the geojson data be stored in a structured format (as JSON or in a spatial database like PostGIS)?
4. Are there size or complexity limits for the GeoJSON file (maximum vertices, file size)?