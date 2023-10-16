# TeXCLIques

A CLI that provides a set of utilities for working with scientific LaTeX documents.

## Installation

This module is available on [PyPI](https://pypi.org/project/texcliques/). To install it, run:

```bash
pip install texcliques
```

Alternatively, you can install it from source using either SSH (recommended) or HTTPS.

To do so, clone this repository and navigate to the root directory.

```bash
git clone git@github.com:dimboump/texcliques      # SSH
git clone https://github.com/dimboump/texcliques  # HTTPS
cd texcliques
```

Then, create a virtual environment and activate it:

```bash
python -m virtualenv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate.bat  # Windows
```

Finally, install the module:

```bash
pip install .
```

## Usage

This module provides a command-line interface (CLI) through the `texcliques` script. To use it, run:

```bash
texcliques [OPTIONS] COMMAND [ARGS]...
```

### Commands

- `extract-refs`: Extract bibliography entries from a LaTeX document or sections thereof given a BibTeX file.

For more information on a specific command, run:

```bash
texcliques COMMAND --help
```

## Contributing

To contribute to texcliques:

1. Fork this repository.
2. Create a new branch following the naming convention `<username>/branch-name`.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Create a [pull request](https://github.com/dimboump/texcliques/compare) to this repository.

## License

This module is licensed under the MIT License. See the `LICENSE` file for more information.
