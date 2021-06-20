from setuptools import setup, find_packages

setup(
    name='phone-scraper',
    version='0.1.0',
    description='Anonymously scrapes onlinesim.ru for new usable phone numbers.',
    author='Thomas Gruebl',
    url='https://github.com/thomasgruebl/phone-scraper',
    packages=find_packages(include='phonescraper'),
    install_requires=[
        'setuptools>=57.0.0',
        'certifi>=2021.5.30',
        'cffi>=1.14.5',
        'chardet>=4.0.0',
        'cryptography>=3.4.7',
        'idna>=2.10',
        'pycparser>=2.20',
        'requests>=2.25.1',
        'termcolor>=1.1.0',
        'torpy>=1.1.6',
        'urllib3>=1.26.5'
    ],
    license='MIT',
    keywords='phone number scraper'
)
