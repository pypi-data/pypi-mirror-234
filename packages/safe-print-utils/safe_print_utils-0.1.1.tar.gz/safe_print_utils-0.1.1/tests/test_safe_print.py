import io
import unittest
from contextlib import redirect_stdout
from safe_print_utils.safe_print_utils import *


class TestSafePrintFunction(unittest.TestCase):

    def test_basic_print(self):
        safe_print("Testing Basic Print...")

        test_string = "Hello, World!"
        expected_output = "Hello, World!\n"

        f = io.StringIO()
        with redirect_stdout(f):
            safe_print(test_string, show_time=False)
        output = f.getvalue()

        self.assertEqual(output, expected_output)

    def test_print_with_error(self):
        safe_print("Testing Print with error...")

        test_string = "Error Occurred!"
        expected_output = "\x1b[31mError Occurred!\x1b[0m\n"

        f = io.StringIO()
        with redirect_stdout(f):
            safe_print(test_string, error=True, show_time=False)
        output = f.getvalue()

        self.assertEqual(output, expected_output)


class TestErrorInfoFunction(unittest.TestCase):

    def test_error_info(self):
        safe_print("Testing Showing of Error Info...")

        try:
            1 / 0  # Trigger ZeroDivisionError
        except Exception as e:
            expected_output_middle = "causes the error. Error message: division by zero\nTraceback:\n"
            expected_output_end = "in test_error_info\n    1 / 0  # Trigger ZeroDivisionError\n\x1b[0m\n"

            f = io.StringIO()
            with redirect_stdout(f):
                error_info(e)
            output = f.getvalue()

            print("Actual output:", repr(output))  # Debugging line

            self.assertTrue(expected_output_middle in output)
            self.assertTrue(output.endswith(expected_output_end))


if __name__ == '__main__':
    unittest.main()
