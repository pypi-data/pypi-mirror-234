from setuptools import setup, find_packages

setup(name='geofunc',
      version='0.1',
      description='Time and date modules capable of handling GPS time',
      url='http://github.com/imo/geofunc',
      author='Benedikt G. Ofeigsson',
      author_email='bgo@vedur.is',
      license='Icelandic Met Office',
      package_dir={'geofunc': 'geofunc'},
      packages=find_packages(),
      install_requires=['pyproj','scipy'],
      zip_safe=False)
