import json
import pyproj
from tqdm import tqdm

def convert_geojson(input_file_path, output_file_path):
    # Define the source and target projections
    proj1 = pyproj.Proj(
    "+proj=lcc +lat_1=59.33333333333334 +lat_2=58 +lat_0=57.51755393055556 +lon_0=24 +x_0=500000 +y_0=6375000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")
    proj2 = pyproj.Proj("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")


    # Open the input file and output file
    with open(input_file_path) as input_file, open(output_file_path, 'w') as output_file:
        # Load the GeoJSON file
        geojson = json.load(input_file)

        # Use Proj4 to perform the coordinate transformation
        for feature in tqdm(geojson['features']):
            # Update the coordinates in the feature
            if feature['geometry']['type'] == 'MultiPolygon':
                feature['geometry']['coordinates'] = [[[pyproj.transform(proj1, proj2, x, y) for x, y in ring] for ring in
                                                        polygon] for polygon in feature['geometry']['coordinates']]
            elif feature['geometry']['type'] == 'Polygon':
                feature['geometry']['coordinates'] = [[pyproj.transform(proj1, proj2, x, y) for x, y in ring] for ring in
                                                       feature['geometry']['coordinates']]

        # Write the transformed GeoJSON to the output file
        json.dump(geojson, output_file)