'''
    Set up for safelog

    Copyright 2018-2023 TopDevPros
    Last modified: 2023-10-07
'''

import os.path
import setuptools

# read long description
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="safelog",
    version="1.8.3",
    author="TopDevPros",
    maintainer="topdevpros",
    description="Safelog is a multithread, multiprocess, multiinstance logging package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="logging multiprocess multithread multi-instance",
    license="GNU General Public License v3 (GPLv3)",
    url="https://codeberg.org/topdevpros/safelog/",
    download_url="https://codeberg.org/topdevpros/safelog/",
    project_urls={
        "Source Code": "https://codeberg.org/topdevpros/safelog/",
    },
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Topic :: System :: Logging",
         ],
    py_modules=["safelog"],
    scripts=['sbin/safelog'],
    entry_points={
    },
    data_files=[],
    setup_requires=['setuptools-markdown'],
    install_requires=['solidlibs'],
    python_requires=">=3.5",
)
