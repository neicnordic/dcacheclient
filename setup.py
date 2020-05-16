# coding: utf-8

"""
    User and administration interaction with dCache  # noqa: E501
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "dcacheclient"
VERSION = "0.0.3"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
#   "urllib3 >= 1.23",
    "six >= 1.10",
    "requests >= 2.6.0",
    "urllib3<1.25,>=1.21.1",
    "certifi",
    "python-dateutil",
    "argcomplete >= 1.9.4",
    "sseclient",
    "liboidcagent >= 0.2.2"]
#    "rucio-clients"]

setup(
    name=NAME,
    version=VERSION,
    description="",
    author_email="support@dCache.org",
    url="https://www.dcache.org",
    keywords=["dCache", "storage"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    User and administration interaction with dCache  # noqa: E501
    """,
    entry_points={
        'console_scripts': ['dcache-admin=dcacheclient.dcache_admin:main',]
    },
)
