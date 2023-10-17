#!/usr/bin/env python
"""
Copyright 2022 The aiXplain models authors
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
Author: Duraikrishna Selvaraju and Michael Lam
Date: May 9th 2022
"""

import os
import sys

from setuptools import setup, find_packages

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of Requests requires at least Python {}.{}, but
you're trying to install it on Python {}.{}. To resolve this,
consider upgrading to a supported Python version.
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

requires = [
    "kserve>=0.10.0",
    "multiprocess==0.70.14", # Support for MacOS multiprocessing.
    "protobuf>=3.19.4",
    "pydantic>=1.9.1",
    "pydub>=0.25.1",
    "requests>=2.28.1",
    "tornado>=6.2", #TODO(krishnadurai): Remove as soon as HTTP errors are refactored
    "validators>=0.20.0"
]

test_requirements = [
    "pytest>=7.1.2",
    "sentencepiece>=0.1.96",
    "torch>=1.13.1",
    "transformers>=4.21.1"
]

about = {}
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "aixplain", "model_interfaces", "__version__.py"), "r") as f:
    exec(f.read(), about)

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="model_interfaces",
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=find_packages(exclude=["test"]),
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    python_requires=">=3.5, <4",
    install_requires=requires,
    license=about["__license__"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ],
    extras_require={
        "tests": test_requirements,
    },
    project_urls={
        "Documentation": "",
        "Source": "https://github.com/aixplain/model-interfaces"
    },
)
