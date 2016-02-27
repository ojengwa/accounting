"""Base Project Module.

The MIT License (MIT)

Copyright (c) 2016 Ojengwa Bernard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re

from accounting.utils import is_str, check_type

__version__ = '0.0.2'


class Accounting(object):
    """docstring for Accounting.

    Attributes:
        settings (dict): The library's settings configuration object. Contains
         default parameters for currency and number formatting
    """

    def __init__(self, options={}):
        """
        Summary.

        Args:
            options (dict, optional): settings configuration object.
        """
        settings = {
            'currency': {
                'symbol': "$",
                'format': "%s%v",
                'decimal': ".",
                'thousand': ",",
                'precision': 2,
                'grouping': 3
            },
            'number': {
                'precision': 0,
                'grouping': 3,
                'thousand': ",",
                'decimal': "."
            }
        }
        if options:
            settings.update(options)

        self.settings = settings

    def _check_currency_format(self, format=None):
        """
        Summary.

        Args:
            format (TYPE, optional): Description

        Returns:
            name (TYPE): Description
        """
        defaults = self.settings['currency']['format']
        if hasattr(format, '__call__'):
            format = format()
        if is_str(format) and re.match('%v', format):

            # Create and return positive, negative and zero formats:
            return {
                'pos': format,
                'neg': format.replace("-", "").replace("%v", "-%v"),
                'zero': format
            }
        elif not format or not format['por'] or not re.match('%v',
                                                             format['pos']):
            self.settings['currency']['format'] = {
                'pos': defaults,
                'neg': defaults.replace("%v", "-%v"),
                'zero': defaults
            }
            return self.settings

        return format

    """
    API Methods.

     Takes a string/array of strings, removes all formatting/cruft and
     returns the raw float value

     Decimal must be included in the regular expression to match floats
      (defaults to Accounting.settings.number.decimal), so if the number uses
      a non-standard decimal
     separator, provide it as the second argument.
     *
     Also matches bracketed negatives (eg. "$ (1.99)" => -1.99)

     Doesn't throw any errors (`None`s become 0) but this may change in future
    """

    def parse(self, value, decimal):
        """
        Summary.

        Args:
            value (TYPE): Description
            decimal (TYPE): Description

        Returns:
            name (TYPE): Description
        """
        # Fails silently (need decent errors):
        value = value or 0

        # Recursively unformat arrays:
        if check_type(value, 'list'):
            return map(lambda val: self.parse(val, decimal))

        # Return the value as-is if it's already a number:
        if check_type(value, 'int') or check_type(value, 'float'):
            return value

        # Default decimal point comes from settings, but could be set to eg.","
        decimal = decimal or self.settings.number.decimal

        # Build regex to strip out everything except digits,
        # decimal point and minus sign
        regex = re.compile("[^0-9-" + decimal + "]", ["g"])
