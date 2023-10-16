#!/usr/bin/env python

import sys
import os
import pkgutil
import subprocess
import mypy.api
import glob

from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand
from pylint.lint import Run

# [ NOTE ]: Directory where this file is located
root_dir = os.path.abspath(os.path.dirname(__file__))
package_name = "KayaModuleSDK"
mypy_config_file = 'conf/setup.mypy.conf'
pylint_config_file = 'conf/setup.pylint.conf'
flake8_config_file = 'conf/setup.flake8.conf'


class MyPyCommand(Command):
    '''
    [ NOTE ]: Custom command to run MyPy checks using `python setup.py mypy`.
    '''
    description = "Run MyPy type checks"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        user_options = [
            '--disallow-untyped-defs', '--config-file', mypy_config_file,
        ]
        user_options.extend(glob.glob('*.py'))
        result = mypy.api.run(user_options)
        print(f'[ MyPy ]: {result}')

        if result[0]:
            print('[ ERROR ]: MyPy found type errors:')
            print(result[0])
            raise SystemExit(1)

        if result[2]:
            print('[ WARNING ]: MyPy found warnings:')
            print(result[2])

class PyLintCommand(Command):
    '''
    [ NOTE ]: Custom command to run PyLint checks using `python setup.py pylint`.
    '''
    description = "Run PyLint type checks"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        user_options = [
            f"--rcfile={pylint_config_file}", "--fail-under=8", package_name,
        ]
        result = Run(user_options)


class Flake8Command(Command):

    description = "Run flake8 checks"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        user_options = ['flake8', '--config', flake8_config_file, '.']
        subprocess.call(user_options)


def add_package_dir_to_path():
    '''
    [ NOTE ]: Add the package directory to the Python path
    '''
    package_dir = os.path.join(root_dir, package_name)
    sys.path.insert(0, package_dir)
    for loader, name, is_pkg in pkgutil.walk_packages([package_dir]):
        full_name = package_name + '.' + name
        if is_pkg:
            path = loader.path
        else:
            path = os.path.dirname(loader.path)
        sys.path.insert(0, path)

# MISCELLANEOUS

# TODO - Check type hints used or break compilation
#MyPyCommand().run()

add_package_dir_to_path()
setup_info = dict(
    name='kaya_module_sdk',
    version='1.24',
    author='Del:Tango',
    author_email='alvearesolutions@gmail.com',
    url='https://kaya.wanolabs.com',
    download_url='http://pypi.python.org/pypi/kaya-module-sdk',
    project_urls={
        'Documentation': 'https://kaya.wanolabs.com.readthedocs.io/en/latest',
        'Source': 'https://github.com/WanoLabs/KayaModuleSDK',
        'Tracker': 'https://github.com/WanoLabs/KayaModuleSDK/issues',
    },
    description='Provides the user a way to create custom strategy modules.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # Package info
    packages=find_packages(),

    # Add _ prefix to the names of temporary build dirs
    options={'build': {'build_base': '_build'}, },
    zip_safe=True,

    test_suite='KAT',
    cmdclass={
        'flake8': Flake8Command,
        'mypy': MyPyCommand,
        'pylint': PyLintCommand,
    },

    install_requires=['flake8', 'mypy', 'pylint'],
    setup_requires=['flake8'],
    entry_points={},
)

setup(**setup_info)


# CODE DUMP

