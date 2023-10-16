from setuptools import setup

VERSION = '0.0.3'
DESCRIPTION = 'A caching library specially designed for FastAPI'
with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="CachiPy",
    version=VERSION,
    author="Ambar Rizvi",
    author_email="<brannstrom9911@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    py_modules=["CachiPy"],
    package_dir={'' : 'CachiPy'},
    install_requires=[],
    keywords=['cache', 'caching', 'API response', 'API caching', 'FastAPI cache', 'FastAPI caching', 'fastapi cacher'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
