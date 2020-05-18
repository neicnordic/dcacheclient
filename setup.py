# coding: utf-8

"""
    User and administration interaction with dCache  # noqa: E501
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "dcacheclient"
VERSION = "0.0.6"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "six >= 1.10",
    "requests >= 2.23.0",
    "certifi",
    "python-dateutil",
    "argcomplete >= 1.11.1",
    "sseclient",
    "liboidcagent >= 0.2.2",
    "rucio-clients"]

setup(
    name=NAME,
    version=VERSION,
    description="",
    author_email="support@dCache.org",
    url="https://github.com/neicnordic/dcacheclient",
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
