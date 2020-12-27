import unittest
import re

from wit import Wit

from main import parse_response


class MyTestCase(unittest.TestCase):
    def test_something(self):
        client = Wit("3OXTFKTQZFCKO3PEYBN3VYS23BDRCVRC")
        front_end_error = "dsd-section\nvocoder-error-message"
        front_end_block = "dsd-section\nvocoder-code-block"
        with open('CommentHelloWorld.wav', 'rb') as f:
            resp = client.speech(f, {'Content-Type': 'audio/wav'})
        resp['intents'][0]['name'] = "AddingComment"
        resp['intents'][0]['confidence'] = 0.8
        resp['entities']['CommentText:CommentText'][0]['body'] = "hello world"
        # assert parse_response(resp) == front_end_block + "\n#hello world"
        self.assertEqual(parse_response(), front_end_block + "\n#hello world")

