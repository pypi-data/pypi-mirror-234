from setuptools import setup

name = "types-bleach"
description = "Typing stubs for bleach"
long_description = '''
## Typing stubs for bleach

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`bleach`](https://github.com/mozilla/bleach) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`bleach`.

This version of `types-bleach` aims to provide accurate annotations
for `bleach==6.1.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/bleach. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `a0047c4266d19ab7fd503ea1c956deee84ed5863` and was tested
with mypy 1.5.1, pyright 1.1.328, and
pytype 2023.8.31.
'''.lstrip()

setup(name=name,
      version="6.1.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/bleach.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['bleach-stubs'],
      package_data={'bleach-stubs': ['__init__.pyi', 'callbacks.pyi', 'css_sanitizer.pyi', 'html5lib_shim.pyi', 'linkifier.pyi', 'sanitizer.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.7",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
