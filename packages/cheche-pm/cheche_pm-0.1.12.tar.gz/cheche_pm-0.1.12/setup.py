#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['numpy','pandas','matplotlib','tqdm','networkx','pydot','plotly','scipy','openpyxl']

test_requirements = [ ]

setup(
    author="Luis Fernando Pérez Armas",
    author_email='luisfernandopa1212@gmail.com',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="A python package dedicated to project scheduling",
    install_requires=requirements,
    license="MIT license",
    long_description= readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='cheche_pm',
    name='cheche_pm',
    packages=find_packages(include=['cheche_pm', 'cheche_pm.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ceche1212/cheche_pm',
    version='0.1.12',
    zip_safe=False,
)
