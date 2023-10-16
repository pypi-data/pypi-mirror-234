#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  11/02/2021 8:16 PM
@Desc    :  exceptions line.
"""
import utx.selenium.utils.six as six


def to_text(val):
    if not isinstance(val, str):
        return val.decode("utf-8")
    return val


class UtxSeleniumException(Exception):
    """
    Base class for errors and exceptions of Airtest-Selenium
    """

    def __init__(self, message=None):
        super().__init__(message)
        self.message = message

    def __str__(self):
        if six.PY2:
            if isinstance(self.message, str):
                return self.message.encode("utf-8")
            else:
                return self.message
        else:
            if isinstance(self.message, bytes):
                return self.message.decode("utf-8")
            else:
                return self.message

    __repr__ = __str__


class IsNotTemplateError(UtxSeleniumException):
    """
    Base class for errors and exceptions of Airtest-Selenium
    """

    def __init__(self, message=None):
        super().__init__(message)

    def __str__(self):
        if six.PY2:
            if isinstance(self.message, str):
                return self.message.encode("utf-8")
            else:
                return self.message
        else:
            if isinstance(self.message, bytes):
                return self.message.decode("utf-8")
            else:
                return self.message

    __repr__ = __str__
