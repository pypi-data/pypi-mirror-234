#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

requires = [
    "setuptools",
    "black >=19",
    "click>=7",
    "click-plugins",
    "boto3",
    "tqdm",
    "requests",
    "sphinx",
    "termcolor",
    "pre-commit",
    "zipp",
    "certifi",
    "docformatter",
    "pyyaml>=6.0",
    "python-dateutil",
    "twine<3",
    "lxml",
    "jinja2",
    "tabulate",
    "psutil",
    "pytz",
    "sagemaker",
    "jupyter",
    "pandas >= 1.3.5",
    "papermill",
    "sqlalchemy-redshift",
    "snowflake-sqlalchemy",
    "sphinx_rtd_theme",
    "pandas-redshift",
    "scikit-learn",
]

setup(
    name="rudderlabs.data.apps",
    version=open("version.txt").read().rstrip(),
    description="Rudderlabs data apps library",
    url="https://github.com/rudderlabs1/rudderlabs.data.apps",
    license="GPLv3",
    # there may be multiple authors (separate entries by comma)
    author="Srinivas",
    author_email="cnu.1439@gmail.com",
    # there may be a maintainer apart from the author - you decide
    # maintainer='?',
    # maintainer_email='email@example.com',
    # you may add more keywords separating those by commas (a, b, c, ...)
    keywords="rudderlabs",
    long_description=open("README.rst").read(),
    # leave this here, it is pretty standard
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        "console_scripts": [
            "rlabs = rudderlabs.data.apps.scripts.rudderlabs:main"
        ],
        "rlabs.cli": [
            "new = rudderlabs.data.apps.scripts.new:new",
            "aws = rudderlabs.data.apps.scripts.aws:aws",
        ],
        "rlabs.aws.cli": [
            "pipeline = rudderlabs.data.apps.scripts.pipeline:pipeline",
            "instance = rudderlabs.data.apps.scripts.aws_ec2_instance:instance",
        ],
        "rlabs.aws.pipeline.cli": [
            "run = rudderlabs.data.apps.scripts.pipeline:run",
            "schedule = rudderlabs.data.apps.scripts.pipeline:schedule",
            "disable_scheduling = rudderlabs.data.apps.scripts.pipeline:disable_scheduling",
            "enable_scheduling = rudderlabs.data.apps.scripts.pipeline:enable_scheduling",
        ],
        "rlabs.aws.instance.cli": [
            "start = rudderlabs.data.apps.scripts.aws_ec2_instance:start",
            "stop = rudderlabs.data.apps.scripts.aws_ec2_instance:stop",
        ],
    },
    # check classifiers, add and remove as you see fit
    # full list here: https://pypi.org/classifiers/
    # don't remove the Blinky framework unless it's not a rudderlabs package
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
