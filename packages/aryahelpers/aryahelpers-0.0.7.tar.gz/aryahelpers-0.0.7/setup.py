"""Setup for aryahelpers modules"""
from setuptools import setup, find_packages

BASE_REPO = 'https://gitlab.com/aryacoreprojects/arya-helpers'

setup(
    name='aryahelpers',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    version='0.0.7',
    description='Arya Helpers Modules',
    long_description='Helper Python modules for Arya + general projects',
    author='Ratnadip Adhikari',
    author_email='ratnadip.adhikari@leoforce.com',
    url=BASE_REPO + '.git',
    download_url=BASE_REPO,
    keywords=['utilities', 'arya', 'helper modules'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities"
    ],
    platforms=['any'],
    install_requires=[],
    # package_data={'aryahelpers': ['configuration/config.helpers.json']}
    include_package_data=True
)
