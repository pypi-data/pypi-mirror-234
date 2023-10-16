import unittest
from logging import getLogger
from pydantic import ValidationError

from certificates_generation_tools.actions.key import KeyAction


class TestKeyAction(unittest.TestCase):
    def setup(self):
        pass

    def _new_action(self, options) -> KeyAction:
        base_options = {"kind": "", "name": "key_action"}
        options = {
            **base_options,
            **options
        }
        return KeyAction("key_action", options, None)

    def test_check_options_error(self):
        with self.assertRaises(ValidationError):
            self._new_action({"bits": "toto"})

    def test_check_options(self):
        self.assertEqual(self._new_action({}).options.bits, 2048)
        self.assertEqual(self._new_action({"bits": "4096"}).options.bits, 4096)
