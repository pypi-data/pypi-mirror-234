'''
    Set up for safeget

    Copyright 2018-2023 TopDevPros
    Last modified: 2023-10-07
'''

import os.path
import setuptools

# read long description
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="safeget",
    version="1.5.6",
    author="TopDevPros",
    maintainer="topdevpros",
    description="Safeget gets and verifies files. It does the security checks that almost everyone skips.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="download verification sigs",
    license="GNU General Public License v3 (GPLv3)",
    url="https://codeberg.org/topdevpros/safeget/",
    download_url="https://codeberg.org/topdevpros/safeget/",
    project_urls={
        "Source Code": "https://codeberg.org/topdevpros/safeget/",
    },
    include_package_data=True,
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "Topic :: System :: Software Distribution",
         ],
    py_modules=["safeget"],
    scripts=['bin/safeget'],
    entry_points={
    },
    setup_requires=['setuptools-markdown'],
    install_requires=[''],
    python_requires=">=3.5",
)
