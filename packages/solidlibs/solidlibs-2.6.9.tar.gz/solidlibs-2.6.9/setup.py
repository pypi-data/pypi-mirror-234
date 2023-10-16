'''
    Set up for open source libraries.

    Copyright 2018-2023 TopDevPros
    Last modified: 2023-10-07
'''

import os.path
import setuptools

# read long description
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="solidlibs",
    version="2.6.9",
    author="TopDevPros",
    maintainer="topdevpros",
    description="Open source python and django enhancements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="logs web-log-parser openssl",
    license="GNU General Public License v3 (GPLv3)",
    url="https://codeberg.org/topdevpros/solidlibs/",
    download_url="https://codeberg.org/topdevpros/solidlibs/",
    project_urls={
        "Source Code": "https://codeberg.org/topdevpros/solidlibs/",
    },
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
         ],
    entry_points={
    },
    setup_requires=['setuptools-markdown'],
    install_requires=[],
    python_requires=">=3.9",
)
