from setuptools import setup

name = "types-pyjks"
description = "Typing stubs for pyjks"
long_description = '''
## Typing stubs for pyjks

This is a PEP 561 type stub package for the `pyjks` package. It
can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pyjks`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pyjks. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `ee6df10dcc22deb1828104182b391a32d41d2f8d` and was tested
with mypy 1.5.1, pyright 1.1.328, and
pytype 2023.8.31.
'''.lstrip()

setup(name=name,
      version="20.0.0.1",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyjks.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-pyasn1'],
      packages=['jks-stubs'],
      package_data={'jks-stubs': ['__init__.pyi', 'bks.pyi', 'jks.pyi', 'rfc2898.pyi', 'rfc7292.pyi', 'sun_crypto.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.7",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
