# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="batch-prediction",
    version="1.0.21",
    description="Batch prediction recipe",
    author="Amit Boke",
    classifiers=["Programming Language :: Python :: 3.8"],
    packages=find_packages(),
    include_package_data=True,
    # install_requires=["refractml", "refractio[all]"],
    install_requires=[],
    python_requires=">=3.8,<3.10"
)
