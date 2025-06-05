import inspect

from yaucl.configholder import ConfigHolder
from yaucl.env import get_env_value


class BaseSectionConfig(ConfigHolder):
    def update_from_env(self, section_key: str, prefix: list[str]) -> None:
        """
        Looks for env variables that correspond to the section passed

        Args:
            section_key: key(name) of this section in the parent config
            prefix: prefixes from parents to construct env variable name

        Returns:

        """
        for key, expected_type in inspect.get_annotations(type(self)).items():
            if key in self.sections:
                section = self.sections[key]
                new_prefix = [*prefix, section_key]
                section.update_from_env(key, prefix=new_prefix)
            else:
                all_key_parts = [*prefix, section_key, key]
                env_var_name = "_".join(all_key_parts)
                env_value = get_env_value(env_var_name, expected_type)
                if env_value is not None:
                    setattr(self, key, env_value)

    def generate_markdown_skeleton(self, name: str) -> str:
        """
        Generates a table with variables belonging to this section.
        Args:
            name: name under which this section is registered

        Returns: string containing a Markdown table

        """
        doc = """
| Option name | Description | Type | Default |
|--------|-------------|------|---------|
"""
        for option, default in self._defaults.items():
            doc += f"""| `{option}` | -- | `{inspect.get_annotations(type(self))[option].__name__}` | `{default}` |\n"""

        for section_name, section in self.sections.items():
            subsection_name = f"{name}.{section_name}"
            doc += f"\n#### {subsection_name}\n{section.generate_markdown_skeleton(subsection_name)}"
        return doc
