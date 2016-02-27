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


def is_str(value):
    """Test whether supplied parameter is a string.

    Given a value, this function will test if it is string both on
    Python 3 and Python 2.

    Args:
        value (object): The value to test.

    Returns:
        True/False (bool): returns True if value is of type string, else False.
    """
    try:
        return isinstance(value, basestring)
    except TypeError:
        return isinstance(value, str)


def check_precision(val, digits):
    try:
        val = round(val, digits)
    except TypeError:
        val = round(val)

    return (lambda val: digits if not val else val)(val)


def clean_type(obj):
    try:
        if str(type(obj)) == "<type 'unicode'>":
            return 'str'
    except TypeError:
        if (type(obj)) == "<type 'str'>":
            return 'str'
    if str(type(obj)) == "<type 'list'>":
        return 'list'
    elif str(type(obj)) == "<type 'dict'>":
        return 'dict'
    elif str(type(obj)) == "<type 'int'>":
        return 'int'
    elif str(type(obj)) == "<type 'float'>":
        return 'float'
    else:
        raise ValueError('Invalid obj argument. Only one of str, int,'
                         ' float, list and dicts are supported.'
                         'Recieved: %s' % str(type(obj)))


def check_type(obj, cls):
    return clean_type(obj) == cls
