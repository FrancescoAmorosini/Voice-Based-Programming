import unittest
import re

from wit import Wit

from main import parse_response


class MyTestCase(unittest.TestCase):
    def test_something(self):
        front_end_error = "dsd-section\nvocoder-error-message\n"
        front_end_block = "dsd-section\nvocoder-code-block\n"
        self.assertEqual(parse_response('CommentHelloWorld.wav'), front_end_block+'# hello world')
        self.assertEqual(parse_response('CreateAnIfStatement.wav'), front_end_block+'if #placeholder :\n\t#placeholder')

