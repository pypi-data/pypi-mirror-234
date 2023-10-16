from setuptools import setup, find_packages

setup(
    name="nasa_visualizations",
    version="0.2",  
    packages=find_packages(),
    install_requires=[
        'numpy',
        'h5py',
        'rasterio',
        'matplotlib',
        'netCDF4',
        'xarray',
        'plotly',
        'pandas',  
        'scikit-learn'  
    ],
    author="zephyr",
    author_email="kunalyadav06112003@gmail.com",
    description="Visualization tools for various NASA datasets including Hyperion EO-1.",
    license="MIT",
    keywords="nasa visualization satellite hyperion",
)
