#!/usr/bin/env python
from setuptools import setup, find_packages


netcatks_dev = [
    "pep8-naming>=0.3.3",   # MIT license
    "flake8>=2.5.1",        # MIT license
    "pyflakes>=1.0.0",      # MIT license
    "nose",
    "coverage",
    "mock>=1.3.0",          # BSD license
    "unittest2>=1.1.0"      # BSD license
]

setup(
    name='NetCatKS',
    version='0.1.3',
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
    extras_require={
        'dev': netcatks_dev,
    },
    install_requires=[
        'Twisted==15.5.0',              # MIT license
        'autobahn>=0.12.1',             # MIT license
        'zope.component==4.2.2',        # Zope Public license
        'zope.event==4.0.3',            # Zope Public license
        'zope.interface==4.1.2',        # Zope Public license
        'colorama',                     # BSD 3-Clause license
        'cryptography>=0.9.3',          # Apache license
        'pyOpenSSL>=0.15.1',            # Apache license
        'pyasn1>=0.1.8',                # BSD license
        'pyasn1-modules>=0.0.7',        # BSD license
        'service_identity>=14.0.0',     # MIT license
    ],
    scripts=['bin/netcatks']
)
