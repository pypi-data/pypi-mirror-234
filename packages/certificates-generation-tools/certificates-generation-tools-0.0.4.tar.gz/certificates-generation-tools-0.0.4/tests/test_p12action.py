import unittest
from logging import getLogger
from pydantic import ValidationError

from certificates_generation_tools.actions.p12 import P12Action


class TestP12Action(unittest.TestCase):
    def setup(self):
        pass

    def _new_action(self, options) -> P12Action:
        base_options = {"kind": "", "name": "p12_action"}
        options = {
            **base_options,
            **options
        }
        return P12Action("p12_action", options, None)

    def _new_action_success(self, options):
        return self._new_action({**options, "private_keyid": "key"})

    def test_check_options_error(self):
        with self.assertRaises(ValidationError):
            self._new_action({})
        with self.assertRaises(ValidationError):
            self._new_action({"private_keyid": "key"})
        with self.assertRaises(ValidationError):
            self._new_action({"private_keyid": "key", "certs_id": []})

    def test_check_options(self):
        action = self._new_action(
            {"private_keyid": "key", "certs_id": ["key"]})
        self.assertEqual(action.options.private_keyid, 'key')
        self.assertEqual(action.options.certs_id, ['key'])
