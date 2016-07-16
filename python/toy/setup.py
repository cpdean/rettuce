import os
import re

from setuptools import setup

PACKAGE_NAME = 'rettuce'

pkg_root = os.path.join(os.path.dirname(__file__), PACKAGE_NAME, '__init__.py')

with open(pkg_root) as v:
    _r = re.compile(r".*__version__ = '(.*?)'", re.S)
    VERSION = _r.match(v.read()).group(1)

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    url='https://github.com/cpdean/rettuce',
    keywords='database',
    author='Conrad Dean',
    author_email='conrad.p.dean@gmail.com',
    license='MIT',
    packages=[PACKAGE_NAME],
    tests_require=['py.test'],
    entry_points={
        "console_scripts": [
            'rettuce-py = rettuce:main',
            'rettuce-server = rettuce:runserver',
        ]
    },
    zip_safe=False,
)
