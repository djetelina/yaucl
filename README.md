# yaucl

[![PyPI - Version](https://img.shields.io/pypi/v/yaucl)](https://pypi.org/project/yaucl/)
![PyPI - License](https://img.shields.io/pypi/l/yaucl)
![PyPI - Downloads](https://img.shields.io/pypi/dm/yaucl)
![GitHub Repo stars](https://img.shields.io/github/stars/DJetelina/yaucl?style=flat&logo=github)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://djetelina.github.io/yaucl)

...so I decided to create `yet another user config library`.

yaucl aims to provide easy-to-use and trivial to implement configuration
for your user-installed applications (such as CLIs, GUIs, TUIs, etc.).

If you need a complicated configuration handling, this might not be the correct library for you.

## Installation

```shell
$ uv add yaucl
```

Or pip, pipenv, poetry, whatever you prefer.

## Why yaucl

- Dataclass-first design
- Full type hint support
- Opinionated defaults
- No runtime template definitions needed
- TOML

### Alternatives

- Generic: [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- User config: [confuse](https://pypi.org/project/confuse/)
- Deployed apps: [dynaconf](https://pypi.org/project/dynaconf/)

See the [Library Comparison](https://djetelina.github.io/yaucl/comparison/) page for a detailed comparison between yaucl and these alternatives.

## The workflow

- Define dataclasses with your default configuration
- Make sure those dataclasses inherit yaucl base classes
- Init the config and then do whatever you want (singleton, passing in arguments...)

## Supported configuration methods

At the moment, yaucl supports [TOML](https://toml.io/en/) and Environmental Variables
as sources for the configuration. While this is extensible (both in yaucl and DIY),
the defaults will probably not change.

Out of the box, you set the defaults; then a config file can overwrite that,
and finally, environmental variables have the last say.
