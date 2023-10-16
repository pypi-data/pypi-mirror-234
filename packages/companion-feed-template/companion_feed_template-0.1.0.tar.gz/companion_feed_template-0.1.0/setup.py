from setuptools import setup, find_packages

setup(
    name='companion_feed_template',
    version='0.1.0',
    packages=find_packages(include=['.', './*']),
    install_requires=[
        'toml',
    ],
)
