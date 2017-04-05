#!/usr/bin/env python3
import os
import json

from setuptools import setup, find_packages

PROJECT_NAME = 'mini-spider'
MODULE_NAME = 'minispider'

here = os.path.abspath(os.path.dirname(__file__))
project_info = json.loads(open(os.path.join(here, 'mini-spider.json')).read())

setup(
    name=project_info['name'],
    version=project_info['version'],

    author=project_info['author'],
    author_email=project_info['author_email'],

    description=project_info['description'],
    long_description=project_info['long_description'],
    keywords=project_info['keywords'],

    url=project_info['url'],
    license=project_info['license'],

    platforms='any',

    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'mini-spider = minispider.__main__:main'
        ]
    }

)
