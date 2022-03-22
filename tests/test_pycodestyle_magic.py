"""
Run under IPython with `ipython tests/test_.*py`.
"""
import unittest
from lintersmagic import pycodestyle

class TestLinenumbers(unittest.TestCase):

    def test_pycodestyle_reports_correct_linenumber(self):
        """Test that pycodestyle reports correct line numbers, and
        accommodates for the cell magic at the top of the cell which is takes
        one line.
        """
        cell = '''print( "oh look kittens!" )'''
        with self.assertLogs() as captured:
            pycodestyle(None, cell)
        self.assertEqual(len(captured.records), 2)  # check that there is only one log message
        self.assertEqual(captured.records[0].getMessage(), "2:7: E201 whitespace after '('")
        self.assertEqual(captured.records[1].getMessage(), "2:26: E202 whitespace before ')'")

    def test_pycodestyle_reports_correct_linenumber_with_leading_empty_lines(self):
        """Test that pycodestyle reports the correct line numbers when there
        are empty lines at the top of the cell, after the cell magic
        but before the actual code.
        """
        cell = '''\nprint( "oh look kittens!" )'''
        with self.assertLogs() as captured:
            pycodestyle(None, cell)
            self.assertEqual(len(captured.records), 2)
            self.assertEqual(captured.records[0].getMessage(), "3:7: E201 whitespace after '('")
            self.assertEqual(captured.records[1].getMessage(), "3:26: E202 whitespace before ')'")

    def test_pycodestyle_reports_three_leading_empty_lines(self):
        """Test that pycodestyle still reports if there are too many empty
        lines at the beginning of the cell.
        """
        cell = '''\n\n\nprint("this is fine")'''
        with self.assertLogs() as captured:
            pycodestyle(None, cell)
            self.assertEqual(len(captured.records), 1)
            self.assertEqual(captured.records[0].getMessage(), "5:1: E303 too many blank lines (3)")

    def test_pycodestyle_leading_comments_skipped_when_reporting(self):
        """Test that leading comments lines are skipped when pycodestyle does
report style issues.
        """
        cell = '''# a comment line\nprint( "oh look kittens!" )'''
        with self.assertLogs() as captured:
            pycodestyle(None, cell)
            self.assertEqual(len(captured.records), 2)
            self.assertEqual(captured.records[0].getMessage(), "3:7: E201 whitespace after '('")
            self.assertEqual(captured.records[1].getMessage(), "3:26: E202 whitespace before ')'")

    def test_pycodestyle_on_skip_errors(self):
        """Test that leading comments lines are skipped when pycodestyle does
report style issues.
        """
        ip = get_ipython()
        ip.history_manager.reset()
        with self.assertLogs() as captured:
            ip.run_cell("%load_ext lintersmagic", store_history=True)
            ip.run_cell("%pycodestyle_on --max_line_length 150 --ignore E225", store_history=True)
            ip.run_cell("print( \"oh look kittens!\" )")
            ip.run_cell("a=\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"",
                        store_history=True)
            self.assertEqual(len(captured.records), 2)
            self.assertEqual(captured.records[0].getMessage(), "2:7: E201 whitespace after '('")
            self.assertEqual(captured.records[1].getMessage(), "2:26: E202 whitespace before ')'")


if __name__ == '__main__':
    unittest.main()
