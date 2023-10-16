#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import setuptools

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('rrmscorer/__main__.py').read(),
    re.M
    ).group(1)

with open("README_pip.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="rrmscorer",
    version=version,
    author="Joel Roca-Martinez, Wim Vranken",
    author_email="joel.roca.martinez@vub.be, wim.vranken@vub.be",
    description="RRM-RNA score predictor",
    license="OSI Approved :: GNU General Public License v3 (GPLv3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer="Joel Roca-Martinez, Wim Vranken",
    maintainer_email="joel.roca.martinez@vub.be, wim.vranken@vub.be",
    url="https://bio2byte.be/rrmscorer",
    project_urls={
        'Documentation': 'https://bitbucket.org/bio2byte/rrmscorer/raw/master/readme.md',
        'Source': 'https://bitbucket.org/bio2byte/rrmscorer/',
        'Say Thanks!': 'https://www.bio2byte.be/b2btools/feedback'
    },
    packages=setuptools.find_packages(include=['rrmscorer']),
    include_package_data=True,
    keywords="proteins RRM RNA predictor sequence bio2byte",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Development Status :: 5 - Production/Stable"
    ],
    python_requires=">=3.9",
    install_requires=[
        "biopython",
        "numpy",
        "pandas",
        "requests",
        "scikit-learn",
        "matplotlib",
        "logomaker"
    ],
    entry_points={
        'console_scripts': [
            'rrmscorer=rrmscorer.__main__:main',
        ]
    }
)
