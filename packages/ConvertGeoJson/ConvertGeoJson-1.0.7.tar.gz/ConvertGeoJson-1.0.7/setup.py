from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='ConvertGeoJson',
    version='1.0.7',
    description='Converts a GeoJSON file from L-EST97 Estonian Coordinate System of 1997 to WGS84',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gleb Redko',
    author_email='gleb.redko@gmail.com',
    url='https://github.com/GlebRed/est97-to-wgs84-convertor',
    packages=find_packages(),
    install_requires=[
        'pyproj',
        'tqdm'
    ],
     entry_points={
        'console_scripts': [
            'convertGeoJson = ConvertGeoJson.convertGeoJson:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)