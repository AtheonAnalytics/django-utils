import setuptools
from setuptools import setup

setup(
    author="Atheon",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Atheon Django Utils",
    install_requires=[
        'django>=3.0, <3.1',
        'requests>=2, <3',
        'python-json-logger>=0.1.11 <1',
        'django-model-utils=>4 < 5'
    ],
    include_package_data=True,
    keywords='django-utils',
    name='django-utils',
    packages=setuptools.find_packages(),
    test_suite='tests',
    version='1.0.0',
)
