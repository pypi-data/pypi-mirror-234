""" Tests
"""
import doctest
import unittest


def test_suite():
    return unittest.TestSuite((doctest.DocTestSuite("plone.schema.jsonfield"),))
