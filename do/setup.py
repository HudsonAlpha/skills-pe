#!/usr/bin/env python2.7
from setuptools import setup

setup(
    name="do",
    version="0.2.0",
    author="Chris King",
    author_email="tchrisking@gmail.com",
    description=("Small python client for basic interactions with digital "
                 "ocean droplets"),
    license="MIT",
    keywords="DigitalOcean cli",
    url="https://github.com/redshadowhero/skills-pe",
    packages=['do'],
    install_requires=['apache-libcloud'],
    entry_points={
        'console_scripts': [
            'dont = do.do:main'
        ]
    }
)
