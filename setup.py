#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

# with open('README.rst') as readme_file:
#     readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()
print(requirements)

setup(
    author="Navin Mohan",
    author_email='navin.mohan@inetlte.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="interact with inet services via python",
    install_requires=requirements,
    # long_description=readme + '\n\n' + history,
    # include_package_data=True,
    name='inetapi',
    packages=find_packages(),
    url='https://github.com/inetdev/inetapi',
    version='2.0',
)
