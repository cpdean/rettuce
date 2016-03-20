import os
import re

from setuptools import setup

PACKAGE_NAME = 'rettucetests'

pkg_root = os.path.join(os.path.dirname(__file__), PACKAGE_NAME, '__init__.py')

with open(pkg_root) as v:
    _r = re.compile(r".*__version__ = '(.*?)'", re.S)
    VERSION = _r.match(v.read()).group(1)

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=[PACKAGE_NAME],
    install_requires=[
        'pytest',
        'docker-py',
        'redis',
    ],
    zip_safe=False,
)
