# _*_ coding: utf-8 _*_
# @author: Drizzle_Zhang
# @file: setup.py.py
# @time: 2023/6/5 12:29

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'scReGAT'
DESCRIPTION = \
    'A GAT-based computational framework to predict long-range gene regulatory relationships'
URL = 'https://github.com/Drizzle-Zhang/scReGAT'
EMAIL = 'zhang_yu18@fudan.edu.cn'
AUTHOR = 'Yu Zhang'
REQUIRES_PYTHON = '>=3.8.3'
VERSION = '0.0.5'

# What packages are required for this module to be executed?
REQUIRED = [
    "numpy", "pandas", "scikit-learn", "scipy", "statsmodels", "anndata", "scanpy", "episcanpy",
    "cosg", "torch", "torch_geometric", "captum", "audtorch", "torch_sparse",
]

# Setting.
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    package_data={NAME: ['data/*']},
    install_requires=REQUIRED,
    license="AGPL-3.0",
    classifiers=["Programming Language :: Python",
        "Programming Language :: Python :: 3"],
)
