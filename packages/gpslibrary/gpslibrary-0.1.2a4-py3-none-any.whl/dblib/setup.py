from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
      name='dblib',
      version='1.0',
      packages = find_packages(),
      description='Database library for use in GPS management',
      url='http://repo.vedur.is:18080/svn/GPS/library/dblib/branches/1.0',
      author='Fjalar Sigurdarson',
      author_email='fjalar@vedur.is',
      )
