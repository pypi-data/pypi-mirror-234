import unittest
from logging import getLogger
from pydantic import ValidationError

from certificates_generation_tools.actions.csr import CsrAction


class TestCsrAction(unittest.TestCase):
    def setup(self):
        pass

    def _new_action(self, options) -> CsrAction:
        base_options = {"kind": "", "name": "csr_action"}
        options = {
            **base_options,
            **options
        }
        return CsrAction("csr_action", options, None)

    def _new_action_success(self, options):
        return self._new_action({**options, "private_keyid": "key"})

    def test_check_options_error(self):
        with self.assertRaises(ValidationError):
            self._new_action({})

    def test_check_options(self):
        self.assertEqual(self._new_action(
            {"private_keyid": "key"}).options.private_keyid, 'key')
