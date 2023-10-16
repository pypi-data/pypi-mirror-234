
# -- import packages: ---------------------------------------------------------
import setuptools
import re
import os
import sys


# -- run setup: ---------------------------------------------------------------
setuptools.setup(
    name="cell_transformer",
    version="0.0.0",
    python_requires=">3.9.0",
    author="Michael E. Vinyard",
    author_email="mvinyard.ai@gmail.com",
    url="https://github.com/mvinyard/cell_transformer",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    description="API for interfacing transformers with singel-cell data.",
    packages=setuptools.find_packages(),
    install_requires=[
        "ABCParse>=0.0.6",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    license="MIT",
)
