from setuptools import setup, find_packages

VERSION = '0.0.8'
DESCRIPTION = 'LIDARpy is a comprehensive Python library tailored for the analysis, manipulation, and interpretation of LIDAR data.'
LONG_DESCRIPTION = 'LIDARpy is a comprehensive Python library tailored for the analysis, manipulation, and interpretation of LIDAR data. This library provides a set of tools for background noise removal, data grouping, bin adjustments, uncertainty computations, and advanced data inversion using both the Klett and Raman methods.'

# Setting up
setup(
    name="lidarpy",
    version=VERSION,
    author="Luan Cordeiro",
    author_email="<luancordeiro@usp.br>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'xarray', 'scipy', 'datetime'],
    keywords=['python', 'lidar', 'clouds', 'data'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
