from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='cparser',
      version='1.0',
      description='Config parser for GPS Station files',
      url='http://repo.vedur.is:18080/svn/GPS/library/cparser/branches/1.0',
      author='Fjalar Sigurdarson',
      author_email='fjalar@vedur.is',
      license='Icelandic Met Office',
      packages=find_packages(),
      include_package_data=True,
      )
