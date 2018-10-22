# -*- mode: pyton coding: utf-8 -*-
"""Setup

Even for PoC, this makes things easier. `pip install -e foo`, `./setup.py test`, etc.
"""

import sys

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    print('Python >= %s.%s required' % REQUIRED_PYTHON)
    sys.exit(1)

from distutils.core import setup

name = 'person_search'

setup(
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    install_requires=['django>=2.1', 'psycopg2', 'requests', 'psycopg2-binary', 'cryptography'],
    name=name,
    version='0.0.1-a',
    provides=[name],
    packages=[name],
    entry_points={
            'console_scripts': ['%s_test=%s.test:main' % (name, name)],
    }
)
