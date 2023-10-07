from setuptools import setup, find_packages

VERSION = '0.0.8'
DESCRIPTION = 'A random base class package'
LONG_DESCRIPTION = 'A random base class package long descriotion'

setup(
    name='bestLibraryEver',
    version=VERSION,
    author='Irakli Nozadze',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python'],
    # install_requires=[
    #     'package1',
    #     'package2',
    # ],
)
