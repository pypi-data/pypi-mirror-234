from setuptools import setup, find_packages

setup(name='pconnect',
      version='1.2',
      description='Connect establishes connections via proxys',
      url='http://repo.vedur.is:18080/svn/GPS/library/pconnect/branches/1.0/',
      author='Fjalar Sigurdarson',
      author_email='fjalar@vedur.is',
      packages = find_packages(),
      scripts=['proxytunnel'],
      install_reqires=['re','getopt'],
      )
