# GeoJSON Converter 🌍
This script converts a **GeoJSON** file from **L-EST97 Estonian Coordinate System of 1997** to **WGS84**.

## Usage
To use this package, you will need to follow these steps:

Install the package by running 

```bash
pip install --target . ConvertGeoJson
``` 
in your terminal or command prompt.

Run the package by running 

```bash
python -m ConvertGeoJson <input_file>.json
```
in your terminal or command prompt.

The converted GeoJSON will be saved to a file called `output.json` in the same directory as the input file.

## Requirements
The script requires the following Python packages:

* pyproj
* tqdm

You can install these packages using pip:

```bash
pip install pyproj tqdm
```

## Author
This script was created by [Gleb Redko](github.com/glebred).

## License
This project is licensed under the [MIT License](LICENSE).