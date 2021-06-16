#!/usr/bin/env python

"""
Copyright 2021 Sven Reissmann <sven.reissmann@rz.hs-fulda.de>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import setuptools


version = open('./VERSION').read().strip()

setuptools.setup(
    license='MIT',

    name='onmsNetbox',
    version=version,

    author='Sven Reissmann',
    author_email='sven.reissmann@rz.hs-fulda.de',

    url='',

    description='A tool for importing network devices from Netbox into OpenNMS',
    long_description=open('README.md').read(),
    keywords='netbox opennms pris',

    install_requires=[
        'yamlreader >= 3.0.0',
        'pynetbox >= 6.1',
        'click >= 7.0',
        'jinja2 >= 2.10'
    ],

    packages=setuptools.find_packages(),

    zip_safe=False,

    package_data={
    },
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'onmsNetbox = onmsNetbox.__main__:main'
        ]
    },
)
