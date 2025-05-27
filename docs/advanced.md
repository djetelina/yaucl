# Advanced usage

## init

Within the init method, you can customize:
- app name
- config "layers" and their order (`load_from`)
- location of the folder for the configuration file (`conf_location`)
- name of the configuration file (`conf_file_name`)

For more detail see [`BaseConfig.init`](./api.md#yaucl.BaseConfig.init)

## Testing

The easiest usage of configuration is as an imported singleton. But when
you want to write tests on top of that, it can cause issues. That's why
yaucl exposes `BaseConfig.load(reset=True)` which resets the configuration to 
the default and loads it again. 

## Generating documentation

yaucl can't do it all for you, but it can generate a skeleton
of the documentation. Instantiate your config class with `init` and then
call [`generate_markdown_skeleton`](./api.md#yaucl.BaseConfig.generate_markdown_skeleton).
Paste the skeleton to your README/documentation and fill in the missing
information, such as option descriptions. Feel free to add examples 
or adjust it as you see fit.

## Extending configuration methods

If you don't want to upstream (or the PR won't get accepted), you can
extend `BaseConfig`. To add a source option, you need to implement
at least `load_from_{source}` method. Keep in mind that the same should
probably be done for `BaseSectionConfig`. Take a look at toml/env loader
methods as an inspiration. For full compatibility, also define `_{source}_doc`.

You can extend yaucl in more ways than just this, if a behavior doesn't suit you,
overload it!

## CLI arguments

yaucl (currently) doesn't support argparse/click/... out of the box because there isn't
"one" way to do it. Another reason being that if arguments were read inside
yaucl, it would be challenging to override the config file, as that's done
at a different time than the actual configuration.
