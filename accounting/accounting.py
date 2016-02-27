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

from accounting.utils import is_str, check_type, is_num

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

    def _check_precision(self, val, base):
        """
        Check and normalise the value of precision (must be positive integer).

        Args:
            val (INT): must be positive integer
            base (INT): Description

        Returns:
            VAL (INT): Description
        """
        if not isinstance(val, int):
            raise TypeError('The first argument must be an integer.')
        val = round(abs(val))
        val = (lambda num: base if is_num(num) else num)(val)
        return val

    def parse(self, value, decimal='.'):
        """
        Summary.

         Takes a string/array of strings, removes all formatting/cruft and
         returns the raw float value

         Decimal must be included in the regular expression to match floats
          (defaults to Accounting.settings.number.decimal),
          so if the number uses a non-standard decimal
         separator, provide it as the second argument.
         *
         Also matches bracketed negatives (eg. "$ (1.99)" => -1.99)

         Doesn't throw any errors (`None`s become 0) but this may change

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
        regex = re.compile("[^0-9-" + decimal + "]")
        unformatted = str(value)
        unformatted = re.sub('/\((.*)\)/', "-$1", unformatted)
        unformatted = re.sub(regex, '', unformatted)
        unformatted = unformatted.replace('.', decimal)
        formatted = (lambda val: unformatted if val else 0)(
            is_num(unformatted))

        return formatted

    def to_fixed(self, value, precision):
        """Implementation that treats floats more like decimals.

        Fixes binary rounding issues (eg. (0.615).toFixed(2) === "0.61")
        that present problems for accounting and finance-related software.

        """
        precision = self._check_precision(
            precision, self.settings['number']['precision'])

        power = pow(10, precision)
        # Multiply up by precision, round accurately, then divide
        power = round(self.parse(value) * power) / power
        return '{0} {1}.{2}f'.format(value, precision, precision)
