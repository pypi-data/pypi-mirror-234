#! python3
import io
import re
import sys
import os.path
from setuptools import setup, find_packages

_srcdir = os.path.abspath(os.path.dirname(__file__))
if _srcdir not in sys.path:
    sys.path.insert(0, _srcdir)

import json2toml


packages = find_packages()
print("[packages]", packages)
print("[version]", json2toml.__version__)

description = json2toml.LONG_USAGE
long_description = description
if os.path.exists("README.md"):
    try:
        with open("README.md", "r") as f:
            long_description = f.read()
            long_description += os.linesep
            long_description += f"```\n{json2toml.get_sys_args().format_help()}\n```"
    except Exception as e:
        print(e)

setup(
    name='json2toml',
    version=json2toml.__version__,
    url='https://git.minieye.tech/nico/wehook-cli',
    license='MIT',
    author='Nico Ning',
    author_email='ningrong@minieye.cc',
    description=(description),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'json2toml',
    ],
    package_data={
        ## If any package contains *.txt files, include them:
        # "": ["_version.txt"],
        "**": ["__init__.py"],
        # "data_proto@*": ["_version.txt"]
    },
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        "click>=8.1.3",
        "json5>=0.9.11",
        "rtoml>=0.9.0",
    ],
    tests_require=[],
    entry_points={
        'console_scripts': [
            'json2toml = json2toml.cli:main'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        # "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
