#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='NetCatKS',
    version='0.1.1b',
    description='Networking with Crossbar, Autobahn and Twisted - Kick Starter',
    author='Dimitar Dimitrov',
    author_email='targolini@gmail.com',
    url='https://github.com/dimddev/NetCatKS',
    packages=find_packages(),
    test_suite='NetCatKS',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Server Tools',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    install_requires=[
        'Twisted==15.4.0',              # MIT license
        'autobahn==0.10.9',             # MIT license
        'lxml==3.4.4',                  # BSD license
        'zope.component==4.2.2',        # Zope Public license
        'zope.event==4.0.3',            # Zope Public license
        'zope.interface==4.1.2',        # Zope Public license
        'xmltodict',                    # ???
        'colorama',                     # BSD 3-Clause license
        'cryptography>=0.9.3',          # Apache license
        'pyOpenSSL>=0.15.1',            # Apache license
        'pyasn1>=0.1.8',                # BSD license
        'pyasn1-modules>=0.0.7',        # BSD license
        'service_identity>=14.0.0',     # MIT license
    ],
    scripts=['bin/netcatks']
)
