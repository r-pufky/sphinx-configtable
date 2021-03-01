# Directive based Sphinx Table extenstion.
Provides a build-validatable method to render tables in sphix documentation.

## Setup
Import extension as a normal sphinx extension.

sphinx/conf.py
```python
extensions = ['sphinx_panels', 'sphinx-configtable']
```

``sphinx_panels`` is required for proper operation.

## Configuration
See each module for specific usage instructions.

A global default may be set for separators and formatting and will be used if a
per-module setting is not set.

See `ct.py` for global defaults.

sphinx/conf.py
```python
ct_separator: Unicode default separator to render for all ms extensions.
    Default: '\N{TRIANGULAR BULLET}'
ct_separator_replace: String default separator to be replace with Unicode
    separator for all ms extensions. Default: '-->'
```

## Modules

| Module    | Description                                         |
|-----------|-----------------------------------------------------|
| `cmdmenu` | Replacement for `guilabel` using global separators. |
| `files`   | File listings.                                      |
| `gpo`     | GPO configuration.                                  |
| `gui`     | GUI navigation and configuration.                   |
| `ports`   | Ports descriptions.                                 |
| `regedit` | Registry configuration.                             | 
