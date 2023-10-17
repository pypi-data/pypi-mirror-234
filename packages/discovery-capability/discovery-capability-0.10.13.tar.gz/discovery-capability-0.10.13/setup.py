# To use a consistent encoding
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

def read(*parts):
    filename = path.join(here, *parts)
    with open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='discovery-capability',
    version=find_version('ds_capability', '__init__.py'),
    description='Data Science to production accelerator',
    long_description=read('README.rst'),
    url='https://github.com/gigas64/discovery-capability',
    author='Gigas64',
    author_email='gigas64@opengrass.net',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Adaptive Technologies',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='Wrangling ML Visualisation Dictionary Discovery Productize Classification Feature Engineering Cleansing',
    packages=find_packages(exclude=['tests', 'guides', 'data', 'jupyter']),
    license='BSD',
    include_package_data=True,
    package_data={
        # If any package contains *.yaml or *.csv files, include them:
        '': ['*.yaml', '*.csv'],
    },
    python_requires='>=3.7',
    install_requires=[
        'discovery-core',
        'pandas>=2',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'scipy',
        'boto3',
        'botocore',
        'fsspec',
        's3fs',
    ],
    extras_require={},
    entry_points={},
    test_suite='tests',
)
