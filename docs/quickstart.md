# Quickstart

## Installation

`uv add yaucl`

## Basic setup

yaucl exposes two classes that should be inherited from.
Dataclass your config, inherit yaucl base classes and profit.

!!! example
    ```python
    import yaucl
    from dataclasses import dataclass, field


    @dataclass
    class SongsConfig(yaucl.BaseSectionConfig):
        genre: str = "metal"


    @dataclass
    class DocumentationConfig(yaucl.BaseConfig):
        timeout: float = 3.14
        colors: str = "rainbow"
        awesome: bool = True
        songs: SongsConfig = field(default_factory=SongsConfig)


    config = DocumentationConfig.init()
    ```

This example, if we assume unix systems, supports `~/.config/documentation/config.toml` and
environmental variables such as `DOCUMENTATION_TIMEOUT` or `DOCUMENTATION_SONGS_GENRE`.

Whether you use config as a singleton that you import elsewhere, or if you
pass it through your application to where it needs to be, you're done.

!!! warning "App name guessing"
    Not specifying your app name is dangerous, keep reading!

### App name

The usage above is, however, a little dangerous because it guesses the name of your
application from the name of your class. Proper minimal usage would actually
call `init` like this:

```python
config = DocumentationConfig.init(app_name="cool_app")
```

The application name then affects the config path and env variables. In this case
the config will now be loaded from `~/.config/cool_app/config.toml` and
env variables will start with `COOL_APP_` instead of `DOCUMENTATION_`
