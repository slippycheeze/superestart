# -*- coding: utf-8 -*-
"""
superestart.

~~~~~~~~~

A supervisord plugin used to autorestart program by specific time.
"""

from setuptools import setup
from superestart import __version__

setup(
    name="superestart",
    version=__version__,
    description="A supervisord plugin used to autorestart program by specific time",
    author="Daniel Pittman, Wang Lei",
    author_email="daniel@rimspace.net, fatelei@gmail.com",
    install_requires=[
        "supervisor >= 4.0.0",
        "croniter >= 1.0.15",
        "argparse-logging >= 2020.11.26",
    ],
    packages=["superestart"],
    zip_safe=False,
    url="https://github.com/slippycheeze/superestart",
    entry_points={
        "console_scripts": [
            "superestart = superestart.main:main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
    license="BSD License"
)
