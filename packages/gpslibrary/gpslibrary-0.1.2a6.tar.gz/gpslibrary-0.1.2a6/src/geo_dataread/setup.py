from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name='geo_dataread',
    version='0.1.0',
    author='Benedikt G. Ofeigsson',
    author_email='bgo@vedur.is',
    description='Reads GPS, multigas, seismic, hydrological datasets',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/gpskings/gpslibrary.git',
    license='Icelandic Met Office',
    package_dir={'geo_dataread': 'geo_dataread'},
    scripts=['bin/read_sil_data'],
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License :: Icelandic Met Office",
        "Operating System :: POSIX",
    ],
)
