"""Test suites."""
import unittest
from accounting.utils import (is_str, is_num, check_precision,
                              check_type, clean_type)
from accounting import Accounting
import sys


class UtilsTestCase(unittest.TestCase):
    """docstring for AccountingTestCase."""

    def setUp(self):
        """
        test up method.

        Returns:
            none (NoneType): None
        """
        self.accounting = Accounting()

    def is_str_test(self):
        self.assertTrue(is_str('Hello'))

    def is_str_error_test(self):
        self.assertRaises(TypeError, is_str(419))

    def int_is_num_test(self):
        self.assertTrue(is_num(419))

    def float_is_num_test(self):
        self.assertTrue(is_num(41.9))

    def check_type_test(self):
        self.assertTrue(check_type([], 'list'))

    def check_precision_test(self):
        self.assertEqual(check_precision(19.20049, 4), 19.2005)

    def clean_type_test(self):
        self.assertEqual(clean_type({}), 'dict')

    unittest.skipIf(sys.version_info[0] > 2, 'Test for unicode type.')
    def unicode_clean_type_test(self):
        self.assertEqual(clean_type(u'Hello'), 'str')

    def str_clean_type_test(self):
        self.assertEqual(clean_type('Hello'), 'str')

    def int_clean_type_test(self):
        self.assertEqual(clean_type(419), 'int')

    def float_clean_type_test(self):
        self.assertEqual(clean_type(419.0), 'float')

