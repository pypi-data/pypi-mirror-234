from __future__ import annotations

import io
import os

import setuptools

# Package metadata.

name = 'neucli'
description = 'Neulabs cli'

# Setup boilerplate below this line.
package_root = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(package_root, 'neucli/version.py')) as fp:
    exec(fp.read(), version)
version = version['__version__']

readme_filename = os.path.join(package_root, 'README.md')
with io.open(readme_filename, encoding='utf-8') as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Neulabs',
    author_email='tech@neulabs.com',
    license='Apache 2.0',
    url='https://github.com/neulabscom/neulabs-cli',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    include_package_data=True,
    zip_safe=False,
    packages=setuptools.find_packages(exclude=['tests*', 'lib*']),
    scripts=['bin/neucli'],
    data_files=['.release-please-manifest.json'],
)
