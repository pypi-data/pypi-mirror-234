import sys
from .convertGeoJson import convert_geojson

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python -m ConvertGeoJson input_file')
        sys.exit(1)

    input_file = sys.argv[1]

    convert_geojson(input_file, 'output.json')