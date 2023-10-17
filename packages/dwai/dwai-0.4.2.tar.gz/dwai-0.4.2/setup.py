#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "jsonpath-ng==1.5.3",
    "twine==4.0.2",
    "tencentcloud-sdk-python==3.0.956"
]

test_requirements = []

setup(
    author="罗涛",
    author_email='luotao@shizhuang-inc.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="云商大模型Python SDK",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dwai',
    name='dwai',
    packages=find_packages(include=['dwai', 'dwai.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tluo-github/dwai',
    version='0.4.2',
    zip_safe=False,
)
