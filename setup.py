# -*- mode: pyton coding: utf-8 -*-
"""Setup

Even for PoC, this makes things easier. `pip install -e foo`, `./setup.py test`, etc.
"""

from distutils.core import setup

name = 'person_search'

setup(
    name=name,
    version='0.0.1-a',
    provides=[name],
    packages=[name],
    entry_points={
            'console_scripts': ['%s_test=%s.test:main' % (name, name)],
    }
)
