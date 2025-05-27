# yaucl

...so I decided to create `yet another user config library`.

yaucl aims to provide easy-to-use and trivial to implement configuration
for your user-installed applications (such as CLIs, GUIs, TUIs, etc.).

If you need a complicated configuration handling, this might not be the correct library for you.

## Why yaucl

- Dataclass-first design
- Full type hint support
- Opinionated defaults
- No runtime template definitions needed
- TOML

### Alternatives

- User config: [confuse](https://pypi.org/project/confuse/)
- Deployed apps: [dynaconf](https://pypi.org/project/dynaconf/)

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
