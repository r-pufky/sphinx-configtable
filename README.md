# Directive based Sphinx Table extenstion.
Provides a build-validatable method to render tables in sphix documentation.

## Setup
Import extension as a normal sphinx extension.

sphinx/conf.py
```python
extensions = ['sphinx-configtable']
```

## Configuration
See each module for specific usage instructions.

A global default may be set for separators and formatting and will be used if a per-module setting is not set.

See `config_table.py` for global defaults.

sphinx/conf.py
```python
ct_separator: Unicode default separator to render for all ms extensions.
    Default: '\N{TRIANGULAR BULLET}'
ct_separator_replace: String default separator to be replace with Unicode
    separator for all ms extensions. Default: '-->'
```

## Modules

| `cmdmenu` | Replacement for `guilabel` using global separators. |
| `generic` | Generic modules.                                    |
| `windows` | Windows specific modules.                           |
| `ubnt`    | Ubiquity specific modules.                          |
