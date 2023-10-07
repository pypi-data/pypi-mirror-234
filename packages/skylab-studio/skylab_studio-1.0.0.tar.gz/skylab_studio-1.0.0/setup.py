"""
SkylabStudio - Python Client
For more information, visit https://studio.skylabtech.ai
"""

from distutils.core import setup
from setuptools import find_packages
# from pathlib import Path
# this_directory = Path(__file__).parent
# long_description = (this_directory / "readme.md").read_text()

with open('README.md') as fp:
    LONG_DESCRIPTION = fp.read()

setup(
    name='skylab_studio',
    version='1.0.0',
    author='skylabtech',
    author_email='info@skylabtech.ai',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/skylab-tech/studio_client_python',
    license='LICENSE.txt',
    description='Skylab Studio python client',
    # long_description = long_description,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    test_suite="skylabtech.test",
    install_requires=[
        "requests >= 2.0.0"
    ],
    extras_require={
        "test": [
            "pytest >= 3.0.5",
            "pytest-cov >= 2.6.1",
            "requests_mock >= 1.5.2",
        ]
    },
    
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Communications :: Email"
    ]
)
