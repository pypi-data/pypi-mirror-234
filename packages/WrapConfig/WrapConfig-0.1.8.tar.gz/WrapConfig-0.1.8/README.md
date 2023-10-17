# Your Project Name

A Python package for managing and persisting configurations with flexibility and ease.

[![PyPI Version](https://img.shields.io/pypi/v/WrapConfig)](https://pypi.org/project/WrapConfig/)
[![License](https://img.shields.io/pypi/l/WrapConfig)](https://github.com/your-username/WrapConfig/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/JulianKimmig/WrapConfig)](https://github.com/JulianKimmig/WrapConfig/stargazers)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [License](#license)

## Features

- **Flexible Configuration**: Easily manage configurations with support for nested keys and subkeys.
- **Persistence**: Persist configurations to various data sources, including in-memory, JSON, and YAML files.
- **Extensible**: Easily extend the package with custom data source support.

## Installation

You can install the package via pip:

```bash
pip install WrapConfig
```

## Usage

```python
from your_project_name import JSONWrapConfig

# Create a JSONWrapConfig instance
config = JSONWrapConfig('config.json')

# Set a configuration value
config.set('section', 'key', value = 'value')

# the value key is not necessary,
config.set('section', 'key', 'value') # results in the same, but is less readable

config.set('section') # will fail, since there is only a key no value



# Get a configuration value
value = config.get('section', 'key')

# Persist changes
config.save()
```

## Configuration

You can configure the package in various ways, including:

- Setting default save behavior.
- Choosing different data sources such as JSON and YAML.

## Examples

For more usage examples, please refer to the examples directory.
(TODO)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
