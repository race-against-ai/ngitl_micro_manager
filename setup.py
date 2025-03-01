import os
from setuptools import find_packages, setup

NAME = 'micro_manager'
VERSION = '0.0.1'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=NAME,
    version=VERSION,
    author="Philipp Altmann",
    description=("Project Manager based on PyQt with QtQuick"),
    license="GPL 3.0",
    keywords="manager pyqt qtquick",
    url="https://github.com/PhilippTrashman",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["micro_manager=backend.main:main"],
    },
    long_description=read('README.md'),
    install_requires=[],
    cmdclass={}
)