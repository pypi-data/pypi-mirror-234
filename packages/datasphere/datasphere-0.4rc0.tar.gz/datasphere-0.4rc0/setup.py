from distutils.core import setup
from setuptools import find_namespace_packages

name = 'datasphere'

setup(
    name=name,
    version='0.4rc0',
    license='Apache-2.0',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
    ],
    tests_require=['pytest', 'pytest-mock'],
    author="Yandex LLC",
    author_email="cloud@support.yandex.ru",
    packages=find_namespace_packages(include=(f'{name}*',)),
    package_data={
        name: ['logs/logging.yaml'],
    },
    install_requires=[
        'pylzy==1.15.0rc2',
        'yandexcloud>=0.233.0',
        'tabulate>=0.9.0',
    ],
    entry_points={
        'console_scripts': [
            'datasphere = datasphere.main:main',
        ],
    },
    python_requires=">=3.8",
    description='Yandex Cloud DataSphere',
    long_description_content_type='text/markdown',
    long_description='Yandex Cloud DataSphere',
)
