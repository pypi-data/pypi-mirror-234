# UnitTestX

[![PyPI Version](https://img.shields.io/pypi/v/unittestx.svg)](https://pypi.org/project/unittestx/)

[![License](https://img.shields.io/pypi/l/unittestx.svg)](https://github.com/fullstack-spiderman/unittestx/blob/main/LICENSE)

[![Python Versions](https://img.shields.io/pypi/pyversions/unittestx.svg)](https://pypi.org/project/unittestx/)

[![Coverage Status](https://coveralls.io/repos/github/fullstack-spiderman/unittestx/badge.svg?branch=main)](https://coveralls.io/github/fullstack-spiderman/unittestx?branch=main)

A custom unittest runner for Python's unittest framework.

## Features

- Custom test result reporting.
- Colorful and informative test status output.
- Support for Python 3.8 and above.

## Installation

You can install UnitTestX using pip:

```bash
pip install unittestx
```

## Usage

Run your tests using UnitTestX by simply invoking the unittestx command.
For example:

```bash
unittestx -s tests -p "test_*.py"
```

You can pass the following arguments to the unittestx command:

```bash
-s or --start-directory: Specify the directory to start test discovery (default is '.').
-p or --pattern: Specify the test file pattern (default is 'test*.py').
For more options and details, use the unittestx --help command.
```

## Contributing

Contributions are always welcome!
Feel free to open issues, submit pull requests, or provide feedback.

## License

[MIT](https://choosealicense.com/licenses/mit/)
