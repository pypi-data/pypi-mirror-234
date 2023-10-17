from __future__ import print_function
from setuptools import setup

import os, sys
import shutil

NAME = "sendgrowl"

def get_version():
    """Get version and version_info without importing the entire module."""
    print("NAME:", NAME)
    path = os.path.join(os.path.dirname(__file__), NAME, '__meta__.py')

    if sys.version_info.major == 3:
        import importlib.util

        spec = importlib.util.spec_from_file_location("__meta__", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        vi = module.__version_info__
        return vi._get_canonical(), vi._get_dev_status()
    else:
        import imp
        vi = imp.load_source("meat", "__meta__.py")
        return vi.__version__, vi.__status__

def get_requirements(req):
    """Load list of dependencies."""

    install_requires = []
    with open(req) as f:
        for line in f:
            if not line.startswith("#"):
                install_requires.append(line.strip())
    return install_requires


def get_description():
    """Get long description."""

    desc = ''

    if os.path.isfile('README.md'):
        with open("README.md", 'r') as f:
            desc = f.read()
    return desc

VER, DEVSTATUS = get_version()

try:
    os.remove(os.path.join(NAME, '__version__.py'))
except:
    pass
try:
    os.remove(os.path.join(NAME, 'sendgrowl.py'))
except:
    pass
shutil.copy2('__version__.py', NAME)
shutil.copy2('sendgrowl.py', NAME)
shutil.copy2('__init__.py', NAME)

import __version__
version = __version__.version

if sys.version_info.major == 3:
    entry_points = {
         "console_scripts": ["sendgrowl3 = sendgrowl:usage",]
    }
else:
    entry_points = {
         "console_scripts": ["sendgrowl = sendgrowl:usage",]
    }

setup(
    name=NAME,
    version=version,
    author = 'Hadi Cahyadi LD',
    author_email = 'cumulus13@gmail.com',
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",    
    description = ('simple send notify to growl'),
    license = 'MIT',
    keywords = "growl windows linux gntp gntplib 23053",
    url = 'https://github.com/cumulus13/sendgrowl',
    project_urls={
        "Documentation": "https://github.com/cumulus13/sendgrowl",
        "Code": "https://github.com/cumulus13/sendgrowl",
    },
    packages = ['sendgrowl'],
    download_url = 'https://github.com/cumulus13/sendgrowl/tarball/master',
    install_requires=[
        'gntplib',
        'argparse',
        'configset'
    ],
    entry_points = entry_points,
    package_data={'': ['__version__.py', 'growl.png', 'sendgrowl.ini']},
    include_package_data=True,
    python_requires=">=2.7",    
    classifiers=[
        'Development Status :: %s' % DEVSTATUS,
        'Environment :: Console',
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
