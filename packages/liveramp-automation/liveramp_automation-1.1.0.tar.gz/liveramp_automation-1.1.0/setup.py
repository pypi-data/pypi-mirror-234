from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

import os

version_ns = {}
with open(os.path.join("liveramp_automation", "__version__.py")) as f:
    exec(f.read(), version_ns)
version = version_ns['__version__']

setup(
    name='liveramp_automation',
    version=version,
    author='Jasmine Qian',
    author_email='jasmine.qian@liveramp.com',
    description="This is the base liveramp_automation_framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LiveRamp/liveramp-automation",
    packages=find_packages(),
    install_requires=[
        'allure-pytest-bdd',
        'allure-python-commons',
        'google',
        'google-api-core',
        'google-auth',
        'google-cloud-bigquery',
        'google-cloud-core',
        'google-cloud-storage',
        'google-crc32c',
        'google-resumable-media',
        'googleapis-common-protos',
        'playwright',
        'pytest',
        'pytest-bdd==6.1.1',
        'pytest-rerunfailures==12.0',
        # Python 3.6 not support this version
        # 'pytest-playwright==0.4.2',
        'pytest-playwright',
        'pytest-json',
        'pytest-json-report',
        'pytest-xdist',
        'PyYAML',
        'requests',
        'retrying==1.3.4',
        'selenium==4.8.3',
        'pandas',
        'db-dtypes',
    ],
)
