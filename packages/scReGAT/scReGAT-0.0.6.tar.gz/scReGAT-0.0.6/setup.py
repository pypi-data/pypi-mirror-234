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
VERSION = '0.0.6'

# What packages are required for this module to be executed?
REQUIRED = [
    "numpy", 
    "pandas",
    "scikit-learn",
    "scipy", 
    "statsmodels",
    "anndata",
    "scanpy",
    "episcanpy==0.3.1",
    "cosg", 
    "torch",
    "pyg_lib",
    "torch_scatter",
    "torch_sparse",
    "torch_cluster",
    "torch_spline_conv",
    "torch_geometric",
    "captum",
    "audtorch",
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
    include_package_data=True,
    package_data={'': ['data/*']},
    install_requires=REQUIRED,
    license="AGPL-3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        ]
    )
