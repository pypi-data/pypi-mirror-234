from typing import Dict, List, Tuple
import unittest
import datetime
from freezegun import freeze_time
from cryptography import x509
from logging import getLogger
from pydantic import ValidationError
from certificates_generation_tools.actions.cert import CertAction, format_extensions


class TestCertAction(unittest.TestCase):
    def setup(self):
        pass

    def _new_action(self, options) -> CertAction:
        base_options = {"kind": "", "name": "cert_action"}
        # "Checking private_keyid error message for certaction")
        options = {
            **base_options,
            **options
        }
        return CertAction("cert_action", options, None)

    def _new_action_success(self, options):
        return self._new_action({**options, "private_keyid": "key", "autosign": True})

    def test_check_options_error(self):
        data_test: List[Tuple[Dict, str]] = [
            ({}, "Checking error message for certaction"),
            ({"private_keyid": "key"},
             "Checking autosign error message for certaction"),
            ({"private_keyid": "key", "autosign": False},
             "Checking autosign error message for certaction"),
            ({"private_keyid": "key", "offsetNotBefore": "toto"},
             "Checking offsetNotBefore error message for certaction"),
            ({"private_keyid": "key", "offsetNotAfter": "toto"},
             "Checking offsetNotAfter error message for certaction"),
            ({"private_keyid": "key", "notBefore": "toto"},
             "Checking notBefore error message for certaction"),
            ({"private_keyid": "key", "notAfter": "toto"},
             "Checking notAfter error message for certaction"),
            ({"private_keyid": "key", "autosign": True, "alternativeNames": "toto", },
             "Checking alternativeNames error message for certaction"),
        ]

        for data in data_test:
            with self.subTest(msg=data[1]):
                with self.assertRaises(ValidationError):
                    self._new_action(data[0])

    def test_autosign(self):
        # "Checking success certaction check_options with notBefore/After and offsetNotBefore/After dates, with autosign"
        options = {
            "private_keyid": "key",
            "notAfter": "2019-05-12",
            "notBefore": "2018-05-12",
            "offsetNotAfter": 10,
            "offsetNotBefore": 30,
            "autosign": True,
        }
        action = self._new_action(options)
        self.assertEqual(action.options.sign_keyid, "key")

    def test_no_autosign(self):
        # "Checking success certaction check_options with notBefore/After and offsetNotBefore/After dates, with autosign"
        options = {
            "private_keyid": "key",
            "autosign": False,
            "sign_keyid": "titi",
        }
        action = self._new_action(options)
        self.assertEqual(action.options.sign_keyid, "titi")

    @freeze_time("05-31-2014")
    def test_dates(self):
        data_test: List[Tuple[Dict, Dict, str]] = [
            (
                {},
                {
                    'offsetNotBefore': 0,
                    'offsetNotAfter': 0,
                    'notBefore': datetime.datetime(2014, 5, 31, 0, 0, 0, 0),
                    'notAfter': datetime.datetime(2014, 5, 31, 0, 0, 0, 0)
                },
                ""
            ),
            (
                {'offsetNotBefore': 100},
                {
                    'offsetNotBefore': 100,
                    'offsetNotAfter': 0,
                    'notBefore': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
                    'notAfter': datetime.datetime(2014, 5, 31, 0, 0, 0, 0)
                },
                ""
            ),
            (
                {'offsetNotBefore': 100},
                {
                    'offsetNotBefore': 100,
                    'offsetNotAfter': 0,
                    'notBefore': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
                    'notAfter': datetime.datetime(2014, 5, 31, 0, 0, 0, 0)
                },
                ""
            ),
            (
                {'offsetNotBefore': 100, 'offsetNotAfter': 100},
                {
                    'offsetNotBefore': 100,
                    'offsetNotAfter': 100,
                    'notBefore': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
                    'notAfter': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000)
                },
                ""
            ),
            (
                {'offsetNotBefore': 100,
                 'offsetNotAfter': 100, 'notAfter': '2016-05-30'},
                {
                    'offsetNotBefore': 100,
                    'offsetNotAfter': 100,
                    'notBefore': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
                    'notAfter': datetime.datetime(2016, 5, 30, 0, 0, 0, 100000)
                },
                ""
            ),
            (
                {'offsetNotBefore': 100,
                 'offsetNotAfter': 100, 'notAfter': '2016-05-30'},
                {
                    'offsetNotBefore': 100,
                    'offsetNotAfter': 100,
                    'notBefore': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
                    'notAfter': datetime.datetime(2016, 5, 30, 0, 0, 0, 100000)
                },
                ""
            ),
            (
                {'offsetNotBefore': 100,
                 'offsetNotAfter': 200, 'notBefore': '2016-05-30'},
                {
                    'offsetNotBefore': 100,
                    'offsetNotAfter': 200,
                    'notBefore': datetime.datetime(2016, 5, 30, 0, 0, 0, 100000),
                    'notAfter': datetime.datetime(2016, 5, 30, 0, 0, 0, 200000)
                },
                ""
            ),
            (
                {'notBefore': '2016-05-31', 'notAfter': '2016-05-30'},
                {
                    'offsetNotBefore': 0,
                    'offsetNotAfter': 0,
                    'notBefore': datetime.datetime(2016, 5, 31, 0, 0, 0, 0),
                    'notAfter': datetime.datetime(2016, 5, 30, 0, 0, 0, 0)
                },
                ""
            ),

        ]
        for data in data_test:
            with self.subTest(data[2]):
                action = self._new_action_success(data[0])
                self.assertEqual(action.options.offsetNotBefore,
                                 data[1]['offsetNotBefore'])
                self.assertEqual(action.options.offsetNotAfter,
                                 data[1]['offsetNotAfter'])
                self.assertEqual(action.options.notBefore,
                                 data[1]['notBefore'])
                self.assertEqual(action.options.notAfter, data[1]['notAfter'])

    def test_ca_extensions(self):
        data_test = [
            ({}, [], ""),
            ({'isCa': False}, [], ""),
            ({'isCa': True}, [
                x509.BasicConstraints(ca=True, path_length=None)
            ], ""),
        ]
        for data in data_test:
            with self.subTest(data[2]):
                action = self._new_action_success(data[0])
                self.assertEqual(action.options.extensions, data[1])
