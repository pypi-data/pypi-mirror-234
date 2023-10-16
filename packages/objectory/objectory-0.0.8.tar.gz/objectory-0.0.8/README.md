# objectory = object + factory

<p align="center">
    <a href="https://github.com/durandtibo/objectory/actions">
        <img alt="CI" src="https://github.com/durandtibo/objectory/workflows/CI/badge.svg">
    </a>
    <a href="https://durandtibo.github.io/objectory/">
        <img alt="Documentation" src="https://github.com/durandtibo/objectory/workflows/Documentation/badge.svg">
    </a>
    <a href="https://github.com/durandtibo/objectory/actions">
        <img alt="Nightly Tests" src="https://github.com/durandtibo/objectory/workflows/Nightly%20Tests/badge.svg">
    </a>
    <a href="https://github.com/durandtibo/objectory/actions">
        <img alt="Nightly Package Tests" src="https://github.com/durandtibo/objectory/workflows/Nightly%20Package%20Tests/badge.svg">
    </a>
    <br/>
    <a href="https://codecov.io/gh/durandtibo/objectory">
        <img alt="Codecov" src="https://codecov.io/gh/durandtibo/objectory/branch/main/graph/badge.svg">
    </a>
    <a href="https://codeclimate.com/github/durandtibo/objectory/maintainability">
        <img src="https://api.codeclimate.com/v1/badges/1fad6e22f2d38335c26d/maintainability" />
    </a>
    <a href="https://codeclimate.com/github/durandtibo/objectory/test_coverage">
        <img src="https://api.codeclimate.com/v1/badges/1fad6e22f2d38335c26d/test_coverage" />
    </a>
    <br/>
    <a href="https://pypi.org/project/objectory/">
        <img alt="PYPI version" src="https://img.shields.io/pypi/v/objectory">
    </a>
    <a href="https://pypi.org/project/objectory/">
        <img alt="Python" src="https://img.shields.io/pypi/pyversions/objectory.svg">
    </a>
    <a href="https://opensource.org/licenses/BSD-3-Clause">
        <img alt="BSD-3-Clause" src="https://img.shields.io/pypi/l/objectory">
    </a>
    <a href="https://github.com/psf/black">
        <img  alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <a href="https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings">
        <img  alt="Doc style: google" src="https://img.shields.io/badge/%20style-google-3666d6.svg">
    </a>
    <br/>
    <a href="https://pepy.tech/project/objectory">
        <img  alt="Downloads" src="https://static.pepy.tech/badge/objectory">
    </a>
    <a href="https://pepy.tech/project/objectory">
        <img  alt="Monthly downloads" src="https://static.pepy.tech/badge/objectory/month">
    </a>
    <br/>
</p>

## Overview

A Python library for general purpose object factories.
In particular, it focuses on dynamic object factory implementations where objects can be registered
dynamically without changing the code of the factory.
An object factory can be used to instantiate an object from its configuration.
The current implementation contains both abstract factory and registry approaches.

**factory**

```pycon
>>> from objectory import factory
>>> class MyClass:
...     pass
...
>>> obj = factory("MyClass")
>>> print(obj)
<__main__.MyClass object at 0x123456789>
```

**[abstract factory](https://durandtibo.github.io/objectory/abstract_factory/)**

```pycon
>>> from objectory import AbstractFactory
>>> class BaseClass(metaclass=AbstractFactory):
...     pass
...
>>> class MyClass(BaseClass):
...     pass
...
>>> obj = BaseClass.factory("MyClass")
>>> print(obj)
<__main__.MyClass object at 0x123456789>
```


**[registry](https://durandtibo.github.io/objectory/registry/)**

```pycon
>>> from objectory import Registry
>>> registry = Registry()
>>> @registry.register()
... class MyClass:
...     pass
...
>>> obj = registry.factory("MyClass")
>>> print(obj)
<__main__.MyClass object at 0x123456789>
```

Please read the [documentation](https://durandtibo.github.io/objectory/) to learn more about these
approaches.

- [Documentation](https://durandtibo.github.io/objectory/)
- [Installation](#installation)
- [Contributing](#contributing)
- [API stability](#api-stability)
- [License](#license)

## Installation

We highly recommend installing
a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
`objectory` can be installed from pip using the following command:

```shell
pip install objectory
```

Please check the [get started page](https://durandtibo.github.io/objectory/get_started) to see other
alternatives to install the library.
The following is the corresponding `objectory` versions and supported dependencies.

| `objectory` | `tornado`    | `python`      |
|-------------|--------------|---------------|
| `0.0.8`     | `>=6.0,<7.0` | `>=3.9,<3.13` |
| `0.0.7`     | `>=6.0,<7.0` | `>=3.9,<3.12` |

## Contributing

Please check the instructions in [CONTRIBUTING.md](.github/CONTRIBUTING.md).

## API stability

:warning: While `objectory` is in development stage, no API is guaranteed to be stable from one
release to the next.
In fact, it is very likely that the API will change multiple times before a stable 1.0.0 release.
In practice, this means that upgrading `objectory` to a new version will possibly break any code
that was using the old version of `objectory`.

## License

`objectory` is licensed under BSD 3-Clause "New" or "Revised" license available
in [LICENSE](LICENSE)
file.
