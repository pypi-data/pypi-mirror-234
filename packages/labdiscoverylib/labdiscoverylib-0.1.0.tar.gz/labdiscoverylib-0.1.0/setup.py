#-*-*- encoding: utf-8 -*-*-
from setuptools import setup
from collections import OrderedDict

classifiers=[
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU Affero General Public License v3",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Education",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

cp_license="GNU AGPL v3"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='labdiscoverylib',
      version='0.1.0',
      description="LabDiscoveryEngine library for creating unmanaged laboratories",
      long_description=long_description,
      long_description_content_type="text/markdown",
      project_urls=OrderedDict((
            ('Documentation', 'https://developers.labsland.com/labdiscoverylib/en/stable/'),
            ('Code', 'https://github.com/labsland/labdiscoverylib'),
            ('Issue tracker', 'https://github.com/labsland/labdiscoverylib/issues'),
      )),
      classifiers=classifiers,
      zip_safe=False,
      author='LabsLand',
      author_email='dev@labsland.com',
      url='https://developers.labsland.com/labdiscoverylib/',
      license=cp_license,
      packages=['labdiscoverylib', 'labdiscoverylib.backends'],
      install_requires=['redis', 'flask', 'six', 'requests'],
     )
