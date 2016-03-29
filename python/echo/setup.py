import os
import re

from setuptools import setup

PACKAGE_NAME = 'eserver'

pkg_root = os.path.join(os.path.dirname(__file__), PACKAGE_NAME, '__init__.py')

with open(pkg_root) as v:
    _r = re.compile(r".*__version__ = '(.*?)'", re.S)
    VERSION = _r.match(v.read()).group(1)

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    keywords='database',
    author='Conrad Dean',
    author_email='conrad.p.dean@gmail.com',
    license='MIT',
    packages=[PACKAGE_NAME],
    tests_require=['py.test', 'docker-py'],
    entry_points={
        "console_scripts": [
            'eserver = {}:main'.format(PACKAGE_NAME),
            'eclient = {}:client'.format(PACKAGE_NAME),
        ]
    },
    zip_safe=False,
)
