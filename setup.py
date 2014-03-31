from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

# workaround for http://bugs.python.org/issue15881
try:
    import multiprocessing
except ImportError:
    pass

setup(
    name="Flask-tiedye",
    version="dev",
    description="Flask Plugin for tiedye-powered Dependency Injection",
    py_modules=["flasktiedye"],
    author="Martin Atkins",
    author_email="mart@degeneration.co.uk",

    test_suite='nose.collector',

    setup_requires=[
        'nose>=1.0',
        'sphinx>=0.5',
    ],
    tests_require=[
        'nose>=1.0',
        'coverage',
        'mock',
        'pep8',
    ],
    install_requires=[
        'Flask',
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
    ]
)
