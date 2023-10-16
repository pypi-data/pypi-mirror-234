# -*- coding: utf-8 -*-
import sys
import os
import json
import re
from datetime import datetime
import traceback
from typing import Any, Union
from colorama import Fore, Back, Style


def safe_print(
        data: Any,
        child_process_label: str = None,
        label_color: str = "RED",
        prefix: str = None,
        prefix_color: str = "GREEN",
        text_color: str = None,
        highlight: bool = False,
        secondary_highlight: bool = False,
        file_path: str = "",
        file_lines_limit: int = 10000,
        show_time: bool = True,
        error: bool = False
) -> None:
    """
    Prints data safely with colored formatting and optional logging to a file.

    :param data: Any, The data to print, will be converted to string.
                 The dict and list will be formatted and indented when printed.
    :param child_process_label: str, Optional label to identify a child process.
    :param label_color: str, Color for child_process_label. Default is "RED".
    :param prefix: str, Optional custom prefix to include in the output.
    :param prefix_color: str, Color for prefix. Default is "GREEN".
    :param text_color: str, Optional color for the main text content.
    :param highlight: bool, If true, highlights the text with yellow background and black text. Default is False.
    :param secondary_highlight: bool, If true, highlights the text with black background and yellow text. Default is False.
    :param file_path: str, Optional file path to save the log.
                      The value should be the string path of file, not a directory.
                      If empty, no log will be saved. Default is "".
    :param file_lines_limit: int, Maximum number of lines to save in the log file. Old lines are trimmed.
                            Default is 10000.
    :param show_time: bool, If true, shows the time as prefix for the print. Default is True.
    :param error: bool, If true, makes the text color red. Default is False.

    :return: None
    """

    data = replace_invalid_utf8_characters(data)

    # Convert data to string
    if isinstance(data, (dict, list)):
        data_str = json.dumps(data, ensure_ascii=False, indent=4)
    else:
        data_str = str(data)

    # Highlight text if required
    if highlight:
        data_str = Fore.BLACK + Back.LIGHTYELLOW_EX + data_str + Style.RESET_ALL

    if secondary_highlight:
        data_str = Fore.LIGHTYELLOW_EX + Back.BLACK + data_str + Style.RESET_ALL

    prefix_str = ''

    if show_time:
        # Get current time in required format
        now = datetime.now()
        current_time = now.strftime("%I:%M %p - %m/%d/%Y").replace(" 0", " ")

        # Build prefix string with colors, child process label, and custom prefix
        prefix_str = f"{Fore.GREEN}[{current_time}]{Style.RESET_ALL} "

    if child_process_label:
        prefix_str += f"{getattr(Fore, label_color.upper())}[Child {child_process_label} Process]{Style.RESET_ALL} "
    if prefix:
        prefix_str += f"{getattr(Fore, prefix_color.upper())}[{prefix}]{Style.RESET_ALL} "

    # Create final output with optional text color
    output = data_str

    if error:
        text_color = "RED"

    if text_color:
        output = getattr(Fore, text_color.upper()) + output + Style.RESET_ALL

    output = prefix_str + output

    # Encode in UTF-8, replace errors with Unicode replacement character
    output_bytes = output.encode('utf-8', errors='replace')

    try:
        # Write bytes to sys.stdout, which handles bytes directly
        sys.stdout.buffer.write(output_bytes)
    except AttributeError:
        # In testing or other environments where sys.stdout is StringIO, write string directly
        sys.stdout.write(output)

    sys.stdout.write("\n")  # Print newline

    # Log to file if file_path is provided
    if file_path:
        # Check if directory exists, create if necessary
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Check if file exists, create if necessary
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding="utf-8", errors="replace"):
                pass

        # Read existing lines from the file
        with open(file_path, "r", encoding="utf-8", errors="replace") as file:
            lines = file.readlines()

        # Remove ANSI escape sequences (color codes)
        plain_output = re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', output)

        # Add new log line at beginning of list, trim old lines if exceeding limit
        lines.insert(0, plain_output + "\n")
        lines = lines[:file_lines_limit]

        # Write updated lines to file
        with open(file_path, "w", encoding="utf-8", errors="replace") as file:
            file.writelines(lines)


def error_info(
        error: Exception,
        file_path: str = "",
        file_lines_limit: int = 10000) -> None:
    """
    Prints detailed information about an error, including line number and traceback.
    Can also log the information to a file.

    :param error: Exception, The exception object that has been caught.
    :param file_path: str, Optional file path to save the log.
                      The value should be the string path of the file, not a directory.
                      If empty, no log will be saved. Default is "".
    :param file_lines_limit: int, Maximum number of lines to save in the log file. Old lines are trimmed.
                            Default is 10000.

    :return: None
    """
    # Get current exception information
    exc_type, exc_value, exc_traceback = sys.exc_info()

    # Check if traceback is available
    if exc_traceback is not None:
        # Format traceback for printing
        formatted_traceback = traceback.format_tb(exc_traceback)

        # Get error message from exception object
        error_message = str(error)

        # Print line number, error message, and full traceback, and log to file if needed
        safe_print(f"Line #: {exc_traceback.tb_lineno} causes the error. "
                   f"Error message: {error_message}\nTraceback:\n{''.join(formatted_traceback)}",
                   error=True, file_path=file_path, file_lines_limit=file_lines_limit)
    else:
        # Print error message if no active traceback, and log to file if needed
        safe_print("No active exception to retrieve traceback from. "
                   "This function should be called within an exception handling block.",
                   error=True, file_path=file_path, file_lines_limit=file_lines_limit)


def replace_invalid_utf8_characters(
        input_data: Union[str, bytes, list, tuple, set, dict, object],
        replacement_character: str = ' ') -> Union[str, list, tuple, set, dict, object]:
    """
    Replaces all characters in the input data that are not valid UTF-8 encoded characters
    with a specified replacement character.

    Parameters:
    input_data (str, bytes, list, tuple, set, dict, object):
        The original data that may contain non-UTF-8 encoded characters.
        It can be text or a collection of texts from any source, including user input or file data.
    replacement_character (str, optional):
        The character used to replace invalid UTF-8 characters. Default is a space.

    Returns:
    Union[str, list, tuple, set, dict, object]:
        A new data with all non-UTF-8 encoded characters replaced by the replacement character.
        The resulting data is guaranteed to be valid UTF-8 and can be used safely in further processing.

    Step-by-step process:
    1. Determine the type of the input data (string, bytes, list, tuple, dictionary, set, object).
    2. If it's a string or bytes, clean the text by encoding and decoding with special error handling.
    3. If it's a list, tuple, set, or dictionary, recursively apply the cleaning function to each element.
    4. If it's an object, attempt to clean attributes that are strings.
    5. Return the cleaned data.
    """

    try:
        # Function to clean a single string
        def clean_string(input_string: str) -> str:
            # Encode to bytes with 'surrogatepass' to preserve invalid Unicode code points
            encoded_bytes_with_invalid_utf8 = input_string.encode('utf-8', 'surrogatepass')
            # Decode back to string with 'replace' to replace invalid UTF-8 sequences
            decoded_string_with_replacement_char = encoded_bytes_with_invalid_utf8.decode('utf-8', 'replace')
            # Replace Unicode replacement characters with the specified replacement character
            cleaned_string_with_replacement_char = decoded_string_with_replacement_char.replace('\ufffd',
                                                                                                replacement_character)
            return cleaned_string_with_replacement_char

        # Handle different data types
        if isinstance(input_data, str):
            return clean_string(input_data)
        elif isinstance(input_data, bytes):
            return clean_string(input_data.decode('utf-8', 'replace'))
        elif isinstance(input_data, (list, tuple, set)):
            return type(input_data)([replace_invalid_utf8_characters(item) for item in input_data])
        elif isinstance(input_data, dict):
            return {key: replace_invalid_utf8_characters(value) for key, value in input_data.items()}
        elif isinstance(input_data, object):
            # Skip objects to avoid errors
            return input_data
        else:
            # Return original if datatype is unsupported
            return input_data

    except Exception as e:
        error_info(e)
        return input_data
