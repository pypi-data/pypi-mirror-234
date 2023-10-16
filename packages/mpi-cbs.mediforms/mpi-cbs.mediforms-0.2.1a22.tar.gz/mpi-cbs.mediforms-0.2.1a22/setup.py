from os import path
from setuptools import find_namespace_packages, setup

from mpi_cbs.mediforms import __version__


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='mpi-cbs.mediforms',
    version=__version__,
    license='AGPLv3+',

    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Stefan Bunde',
    author_email='stefanbunde+git@posteo.de',

    url='https://bitbucket.org/huscy/mediforms',

    packages=find_namespace_packages(include=['mpi_cbs.*']),
    include_package_data=True,

    install_requires=[
        'Django>=3.2',
        'weasyprint==53',
    ],
    extras_require={
        'development': ['psycopg2-binary'],
        'testing': ['tox', 'watchdog==0.9']
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
    ],
)
