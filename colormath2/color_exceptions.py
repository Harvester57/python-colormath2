# -*- coding: utf-8 -*-
"""
This module contains exceptions for use throughout the L11 Colorlib.
"""


class ColorMath2Exception(Exception):
    """
    Base exception for all colormath2 exceptions.
    """

    pass


class UndefinedConversionError(ColorMath2Exception):
    """
    Raised when the user asks for a color space conversion that does not exist.
    """

    def __init__(self, cobj, cs_to):  # noqa: B042
        self.message = "Conversion from %s to %s is not defined." % (cobj, cs_to)
        super(UndefinedConversionError, self).__init__(self.message)


class InvalidIlluminantError(ColorMath2Exception):
    """
    Raised when an invalid illuminant is set on a ColorObj.
    """

    def __init__(self, illuminant):
        self.message = "Invalid illuminant specified: %s" % illuminant
        super(InvalidIlluminantError, self).__init__(self.message)


class InvalidObserverError(ColorMath2Exception):
    """
    Raised when an invalid observer is set on a ColorObj.
    """

    def __init__(self, cobj):
        observer = cobj.observer if hasattr(cobj, "observer") else cobj
        self.message = "Invalid observer angle specified: %s" % observer
        super(InvalidObserverError, self).__init__(self.message)
