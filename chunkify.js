// chunkify.js: 
//      Convert a single linestring into a set of linestrings of a specified length.
//
//      Input: A geojson featurecollection consisting of a single feature, with a geometry of one linestring.
//      Output: A geojson featurecollection consisting of a set of features with one linestring each. The first point in each linestring is the same as the last point in the previous linestring.
//

const fs = require('fs');
const turf = require('turf');
const lineChunk = require('@turf/line-chunk');

let inFile = 'pct.geojson';
let outFile = 'pct-chunks.geojson';
let chunkSize = 10;
let chunkUnits = 'miles';

// Load trail data as single linestring.
let inData = fs.readFileSync(inFile);
let trailJson = JSON.parse(inData);

// Create set of linestrings of length chunkSize chunkUnits.
chunks = lineChunk(turf.lineString(trailJson['features'][0]['geometry']['coordinates']), chunkSize, {units: chunkUnits}); 

// Save the chunked trail. 
let outData = JSON.stringify(chunks);
fs.writeFileSync(outFile, outData);