from __future__ import absolute_import
import unittest
from lxml.doctestcompare import LXMLOutputChecker
from doctest import Example


class XmlTest(unittest.TestCase):
    """http://stackoverflow.com/a/7060342"""
    def assertXmlEqual(self, got, want):
        checker = LXMLOutputChecker()
        if not checker.check_output(want, got, 0):
            message = checker.output_difference(Example("", want), got, 0)
            raise AssertionError(message)
