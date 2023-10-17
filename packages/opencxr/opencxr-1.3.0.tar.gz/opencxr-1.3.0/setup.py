#!/usr/bin/env python

import os
from typing import Dict

from setuptools import find_packages, setup

NAME = "opencxr"
REQUIRES_PYTHON = ">=3.7"

with open("README.md", "r") as readme_file:
    readme = readme_file.read()


requirements = [
    # "pandas!=0.24.0",
    # "imageio",
    # "cookiecutter",
    # "click",
    # "scipy",
    "wget==3.2",
    "tensorflow==2.14.0",
    "SimpleITK==2.3.0",
    "keras==2.14.0",
    "pydicom==2.4.3",
    "pypng==0.20220715.0",
    "scikit-image==0.22.0",
    "scikit-build==0.17.6",
    "numpy==1.26.0",
]

# test_requirements = ["pytest", "pytest-cov", "pytest-xdist", "pytest-randomly"]

# here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="opencxr",
    author="Keelin Murphy",
    author_email="keelin.murphy@radboudumc.nl",
    description=(
        "a collection of algorithms for processing of chest radiograph (CXR) images"
    ),
    install_requires=requirements,
    # include_package_data=True,
    license="Apache 2.0",
    long_description="a collection of algorithms for processing of chest radiograph (CXR) images",
    keywords="opencxr",
    url="https://github.com/DIAGNijmegen/opencxr",
    packages=find_packages(),
    version="1.3.0",
)
