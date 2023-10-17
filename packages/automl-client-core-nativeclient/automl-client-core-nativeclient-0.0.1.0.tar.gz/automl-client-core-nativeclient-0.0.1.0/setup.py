# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Python setup module for the AutoML native client package."""
import os
from setuptools import setup, find_packages
import shutil

NAME = "automl-client-core-nativeclient"

_major = '0.0'
_minor = '0.0'

shutil.copy('../.license', 'LICENSE.txt')

if os.path.exists('../major.version'):
    with open('../major.version', 'rt') as bf:
        _major = str(bf.read()).strip()

if os.path.exists('../minor.version'):
    with open('../minor.version', 'rt') as bf:
        _minor = str(bf.read()).strip()

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "automl", "client", "core", "nativeclient", "_version.py"), "w+") as verfile:
    verfile.write('ver = \"{}.{}\"\n'.format(_major, _minor))

VERSION = '{}.{}'.format(_major, _minor)
SELFVERSION = VERSION
if os.path.exists('patch.version'):
    with open('patch.version', 'rt') as bf:
        _patch = str(bf.read()).strip()
        SELFVERSION = '{}.{}'.format(VERSION, _patch)


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: Other/Proprietary License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS',
    'Operating System :: POSIX :: Linux'
]


# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    '{}~={}'.format('azureml-core', VERSION),
    '{}~={}'.format('azureml-automl-core', VERSION),
    '{}~={}'.format('azureml-automl-runtime', VERSION),
    '{}~={}'.format('azureml-interpret', VERSION),
    '{}~={}'.format('azureml-telemetry', VERSION),
    'numpy>=1.16.0,<=1.21.6; python_version<"3.8"',
    'numpy>=1.16.0,<=1.23.5; python_version>="3.8"',
    'scipy>=1.0.0,<=1.11.0',
    'scikit-learn>=1.0.0,<=1.1.3',
    'pandas==1.3.5',
    'adal<1.3.0',
    'psutil>=5.2.2,<6.0.0',
    'requests>=2.17.0,<3.0.0',
    'jsonschema>=2.6.0,<3.0.0',
    'lightgbm>=2.0.11,<=3.2.1',
    'sklearn_pandas>=1.4.0,<=1.7.0',
    'applicationinsights<0.12.0'
]

with open('README.rst', 'r', encoding='utf-8') as f:
    README = f.read()
with open('HISTORY.rst', 'r', encoding='utf-8') as f:
    HISTORY = f.read()
with open('../.inlinelicense', 'r', encoding='utf-8') as f:
    inline_license = f.read()

setup(
    name=NAME,
    version=SELFVERSION,
    description="AutoML native client implementation",
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/x-rst',
    author='Microsoft Corp',
    license=inline_license,
    url='https://docs.microsoft.com/python/api/overview/azure/ml/?view=azure-ml-py',
    classifiers=CLASSIFIERS,
    install_requires=REQUIRES,
    python_requires=">=3.7,<4",
    packages=find_packages(exclude=["*.tests", "*.scripts", "tests", "scripts"]),
    include_package_data=True,
    zip_safe=False
)
