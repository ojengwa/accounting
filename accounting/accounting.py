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

from .utils import is_str, check_type, is_num


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

    def _check_precision(self, val, base=0):
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

    def parse(self, value, decimal=None):
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

    def format(self, number, **kwargs):
        """Format a given number.

        Format a number, with comma-separated thousands and
        custom precision/decimal places

        Localise by overriding the precision and thousand / decimal separators
        2nd parameter `precision` can be an object matching `settings.number`

        Args:
            number (TYPE): Description
            precision (TYPE): Description
            thousand (TYPE): Description
            decimal (TYPE): Description

        Returns:
            name (TYPE): Description
        """
        # Resursively format lists
        if check_type(number, 'list'):
            return map(lambda val: self.format(val, **kwargs))
        # Clean up number
        number = self.parse(number)

        # Build options object from second param (if object) or all params,
        # extending defaults
        if check_type(kwargs, 'dict'):
            options = (self.settings['number'].update(kwargs))

        # Clean up precision
        precision = self._check_precision(options['precision'])
        negative = (lambda num: "-" if num < 0 else "")(number)
        base = str(int(self.to_fixed(abs(number) or 0, precision)), 10)
        mod = (lambda num: len(num) % 3 if len(num) > 3 else 0)(base)

        # Format the number:
        num = negative + (lambda num: base[0:num] if num else '')(mod)

        num += re.sub('/(\d{3})(?=\d)/g', '$1' +
                      options['thousand'], base[mod:])
        num += (lambda val: options[
            'decimal'] + self.to_fixed(abs(number), precision)
            .split('.')[1] if val else '')(precision)

        return num

    def as_money(self, number, **options):
        """Format a number into currency.

        Usage: accounting.formatMoney(number, symbol, precision, thousandsSep,
                                      decimalSep, format)
        defaults: (0, "$", 2, ",", ".", "%s%v")
        Localise by overriding the symbol, precision,
        thousand / decimal separators and format
        Second param can be an object matching `settings.currency`
        which is the easiest way.

        Args:
            number (TYPE): Description
            precision (TYPE): Description
            thousand (TYPE): Description
            decimal (TYPE): Description

        Returns:
            name (TYPE): Description
        """
        # Resursively format arrays
        if isinstance(number, list):
            return map(lambda val: self.as_money(val, **options))

        # Clean up number
        decimal = options.get('decimal')
        number = self.parse(number, decimal)

        # Build options object from second param (if object) or all params,
        # extending defaults
        if check_type(options, 'dict'):
            options = (self.settings['currency'].update(options))

        # Check format (returns object with pos, neg and zero)
        formats = self._check_currency_format(options['format'])

        # Choose which format to use for this value
        use_format = (lambda num: formats['pos'] if num > 0 else formats[
                      'neg'] if num < 0 else formats['zero'])(number)
        precision = self._check_precision(number, options['precision'])
        thousands = options['thousand']
        decimal = options['decimal']
        formater = self.format(abs(number), precision, thousands, decimal)

        # Return with currency symbol added
        amount = use_format.replace(
            '%s', options['symbol']).replace('%v', formater)

        return amount
