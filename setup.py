#!/usr/bin/env python
from setuptools import setup, find_packages

version = '2.0.20'

url = 'https://github.com/teleprint-me/coinbasepro-python'

install_requires = [
    'requests',
    'websocket-client',
    'pymongo',
    'sortedcontainers'
]

tests_require = [
    'pytest',
    'python-dateutil',
]

keywords = [
    'cbpro', 'gdax', 'gdax-api', 'orderbook', 'trade',
    'bitcoin', 'ethereum', 'BTC', 'ETH', 'client', 'api', 'wrapper',
    'exchange', 'crypto', 'currency', 'trading', 'trading-api',
    'coinbase', 'pro', 'prime', 'coinbasepro'
]

download_url = \
    'https://github.com/teleprint-me/coinbasepro-python/archive/refs/tags/2.0.20.zip'

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='cbpro',
    version=version,
    author='Daniel Paquin',
    author_email='dpaq34@gmail.com',
    license='MIT',
    url=url,
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
    },
    description='The unofficial Python client for the Coinbase Pro API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url=download_url,
    keywords=keywords,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
