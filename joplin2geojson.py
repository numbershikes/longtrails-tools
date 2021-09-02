# Export a Joplin folder to a GeoJSON file, via the Joplin Data API.
#
#	* The Joplin Data API is documented at https://joplinapp.org/api/references/rest_api/
#	* baseurl is the url of the Joplin Data Api ("Web Clipper Service"), including port.
#       * Ensure that the Joplin Data API server is running:
#           * On Joplin for Windows: Tools -> Options -> Web Clipper -> Enable the clipper service.
#           * On Joplin Terminal for Linux: joplin server start &>/dev/null &
#               * The "&>/dev/null &" suppresses the Joplin server's logging, which will otherwise echo to STDOUT for every call.
#	* folder is the Joplin folder id, available via the data API. Joplin Notebooks are called 'folders' internally.
#       * To get a list of all folders: http://localhost:41184/folders?token=your_api_token_here
#	* fields is a list of note fields to include in the export. Available values are listed in the data API documentation at the above URL.
#	* token is available from Joplin:
#		* Joplin for Windows -> Tools -> Options -> Web Clipper -> Advanced Option -> Authorisation Token.
#		* Joplin Terminal Linux: $ joplin config api.token
#	* out_file is the name of the file to which the final GeoJSON will be written.
#
# Prior to running this script, the Joplin Data API server ("Web Clipper Service") must be started.
#

import requests
import json

baseurl = "http://localhost:41184"
folder = "your_joplin_folder_id_here"
fields = "fields=title,body,id,created_time,updated_time,longitude,latitude"
token = "token=your_token_here"
#json_outfile = '/path/to/outfile/joplin_data.json'
#json_infile = '/path/to/infile/joplin_data.json'
geojson_outfile = '/path/to/geojson/joplin_data.geojson'

page = 1
print("page 1")

r = requests.get(baseurl + "/folders/" + folder + "/notes?" + fields + "&page=1&" + token).json()
data = r["items"]
while(r["has_more"] == True):
    page += 1
    print("page " + str(page))
    r = requests.get(baseurl + "/folders/" + folder + "/notes?" + fields + "&page=" + str(page) + "&" + token).json()
    data.extend(r["items"])

# Optionally, write the JSON to disk.
#with open(json_outfile, "w") as f:
#    json.dump(data, f)

# Optionally, load JSON from disk. Note that this will overwrite the data just pulled from the API.
#with open(json_infile, "r") as f:
#    data = json.load(f)

# Hattip https://gis.stackexchange.com/a/74046
geojson = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "geometry" : {
            "type": "Point",
            "coordinates": [d["longitude"], d["latitude"]],
            },
        "properties" : d,
    } for d in data]
}

with open(geojson_outfile, "w") as f:
    json.dump(geojson, f)
