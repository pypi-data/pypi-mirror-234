from setuptools import setup, find_packages

setup(
    name="nasa_visualizations",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'h5py',
        'rasterio',
        'matplotlib',
        'netCDF4',
        'xarray',
        'plotly'
    ],
    author="zephyr",
    author_email="kunalyadav06112003@gmail.com",
    description="Visualization tools for various NASA datasets.",
    license="MIT",
    keywords="nasa visualization satellite",
)
