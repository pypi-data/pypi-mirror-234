# chinaski

Detect email addresses in files.
A tribute to the novel [Post Office](https://en.wikipedia.org/wiki/Post_Office_(novel)) from Charles Bukowski.

[![PyPI](https://img.shields.io/pypi/v/chinaski)](https://pypi.org/project/chinaski/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/w0rmr1d3r/chinaski)](https://github.com/w0rmr1d3r/chinaski/releases)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/chinaski)
[![PyPi downloads](https://img.shields.io/pypi/dm/chinaski?label=PyPi%20downloads)](https://pypistats.org/packages/chinaski)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install chinaski.

```bash
pip install chinaski
```

## Usage

### As CLI

```text
Usage: python -m chinaski [OPTIONS] PATH_TO_FILE_OR_DIR

  Detect emails addresses in files.

  PATH_TO_FILE_OR_DIR: Path to single file or directory to scan.

Options:
  --help  Show this message and exit.
```

Example:

```bash
# Detect in only 1 file
python -m chinaski ./file.txt

# Detect in a directory
python -m chinaski path/to/dir
```

### Inside your code

```python
from chinaski.henry import core

if __name__ == '__main__':
    core("file.txt")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPLv3](LICENSE)
