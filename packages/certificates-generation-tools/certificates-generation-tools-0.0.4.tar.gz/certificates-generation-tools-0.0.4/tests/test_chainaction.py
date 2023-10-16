import unittest
from logging import getLogger
from pydantic import ValidationError

from certificates_generation_tools.actions.chain import ChainAction


class TestChainAction(unittest.TestCase):
    def setup(self):
        pass

    def _new_action(self, options) -> ChainAction:
        base_options = {"kind": "", "name": "chain_action"}
        options = {
            **base_options,
            **options
        }
        return ChainAction("chain_action", options, None)

    def _new_action_success(self, options):
        return self._new_action({**options, "private_keyid": "key"})

    def test_check_options_error(self):
        with self.assertRaises(ValidationError):
            self._new_action({})
        with self.assertRaises(ValidationError):
            self._new_action({"certs_id": []})

    def test_check_options(self):
        self.assertEqual(self._new_action(
            {"certs_id": ["key"]}).options.certs_id, ['key'])
