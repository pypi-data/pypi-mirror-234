from setuptools import setup
from setuptools import find_packages

VERSION = '1.0.6.4'
AUTHOR='eegion'
EMAIL='hehuajun@eegion.com'

option = {
    "build_exe": {
        "excludes":["test", "main"],
        'packages':['utils','device','x7base','network']
    }
}

setup(
    name='qldev',  # package name
    version=VERSION,  # package version
    author=AUTHOR,
    author_email=EMAIL,
    description='api for x7 box since v1.2.2',  # package description
    packages=find_packages(),
    install_requires=['loguru'],
    package_data={
        "":["*.txt", "*.md"]
    },
    zip_safe=False
)