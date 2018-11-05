# coding: utf-8

"""
    User and administration interaction with dCache  # noqa: E501
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "dcacheclient"
VERSION = "0.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "urllib3 >= 1.15",
    "six >= 1.10",
    "requests >= 2.19.1",
    "certifi",
    "python-dateutil",
    "argcomplete >= 1.9.4"]

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
        'console_scripts': ['dcache-admin=dcacheclient.dcache_admin:main']
        },
)
