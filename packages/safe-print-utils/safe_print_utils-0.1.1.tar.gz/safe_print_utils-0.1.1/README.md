# Safe Print Logging Utilities

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
   - [Requirements](#requirements)
   - [Installation Steps](#installation-steps)
   - [Installing with pip](#installing-with-pip)
3. [Usage](#usage)
   1. [`safe_print`](#1-safe_print)
      - [Description](#description)
      - [Parameters](#parameters)
      - [Example](#example)
   2. [`error_info`](#2-error_info)
      - [Description](#description-1)
      - [Parameters](#parameters-1)
      - [Example](#example-1)
   3. [`replace_invalid_utf8_characters`](#3-replace_invalid_utf8_characters)
      - [Description](#description-2)
      - [Parameters](#parameters-2)
      - [Example](#example-2)
   4. [Additional Usage Notes](#additional-usage-notes)
4. [Contributors](#contributors)

## Overview

The Safe Print Logging Utilities is a Python script providing enhanced printing functionality with colorful formatting, logging capability, and handling of UTF-8 encoding issues across various data types. 

The Utilities define three main functions:
- `safe_print`: Augments print functionality.
- `error_info`: Logs detailed error information.
- `replace_invalid_utf8_characters`: Mitigates issues with invalid UTF-8 characters.

## Installation

### Requirements
- Python 3.x
- `colorama` package

### Installation Steps

1. Ensure Python is installed on your machine.
2. Install the `colorama` package using pip:
    ```bash
    pip install colorama
    ```
3. Integrate the script into your project.

### Installing with pip
Since the package is available on PyPI, you can install it using pip with the following command:
```bash
pip install safe_print_utils
```

## Usage

### 1. `safe_print`

#### Description
Prints data with colorful formatting and logging options.

#### Parameters
- `data`: Data to print, formatted/indented for dicts and lists.
- `child_process_label`: (Optional) Label identifying a child process.
- `label_color`: Color for `child_process_label` (Default: "RED").
- `prefix`: (Optional) Custom output prefix.
- `prefix_color`: Prefix color (Default: "GREEN").
- `text_color`: (Optional) Main text color.
- `highlight`: Flag to highlight text with yellow background and black text (Default: False).
- `secondary_highlight`: Flag to highlight text with black background and yellow text (Default: False).
- `file_path`: (Optional) File path for logging (Default: "").
- `file_lines_limit`: Max lines in log file, older lines are removed (Default: 10000).
- `show_time`: Flag to prefix output with the time (Default: True).
- `error`: Flag to make text color red (Default: False).

#### Example
```python
safe_print("Hello, World!", prefix="Info", prefix_color="GREEN")
```

### 2. `error_info`

#### Description
Prints and optionally logs detailed error information, including line number and traceback.

#### Parameters
- `error`: Caught exception object.
- `file_path`: (Optional) Log file path (Default: "").
- `file_lines_limit`: Max lines in log file, older lines are removed (Default: 10000).

#### Example
```python
try:
    1/0
except Exception as e:
    error_info(e)
```

### 3. `replace_invalid_utf8_characters`

#### Description
Replaces invalid UTF-8 characters within various data types.

#### Parameters
- `input_data`: Data containing potential non-UTF-8 encoded characters.
- `replacement_character`: Character replacing invalid UTF-8 characters (Default: ' ').

#### Example
```python
cleaned_data = replace_invalid_utf8_characters("some_data_with_invalid_utf8")
```

### Additional Usage Notes
- Ensure text/log file encoding compatibility with UTF-8.
- Ensure correct and writable file path/directory when logging with `safe_print`.

## Contributors
- SyntaxSurge (https://syntaxsurge.com)
