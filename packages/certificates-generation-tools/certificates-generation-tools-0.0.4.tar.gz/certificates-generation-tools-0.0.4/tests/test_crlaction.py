from typing import Dict, List, Tuple
import unittest
import datetime
from logging import getLogger
from freezegun import freeze_time
from pydantic import ValidationError

from certificates_generation_tools.actions.crl import CrlAction, RevokedCerts


class TestCrlAction(unittest.TestCase):
    def setup(self):
        pass

    def _new_action(self, options) -> CrlAction:
        base_options = {"kind": "", "name": "crl_action"}
        # "Checking private_keyid error message for certaction")
        options = {
            **base_options,
            **options
        }
        return CrlAction("cert_action", options, None)

    def _new_action_success(self, options):
        return self._new_action({**options, "sign_keyid": "key", "ca_id": "ca"})

    def test_check_options_error(self):
        data_test: List[Tuple[Dict, str]] = [
            ({}, "Checking sign_keyid error message for crlaction"),
            ({"sign_keyid": "key", "offsetValidityTime": "toto"},
             "Checking offsetValidityTime error message for crlaction"),
            ({"sign_keyid": "key", "offsetExpirationTime": "toto"},
             "Checking offsetExpirationTime error message for crlaction"),
            ({"sign_keyid": "key", "validityTime": "toto"},
             "Checking validityTime error message for crlaction"),
            ({"sign_keyid": "key", "expirationTime": "toto"},
             "Checking expirationTime error message for crlaction"),
            ({"sign_keyid": "key", "revokedCerts": [{"revocationDate": "2020-07-06"}], },
             "Checking cert_id error message for revoked certificate in crlaction"),
            ({"sign_keyid": "key", "revokedCerts": [{"cert_id": "key", "revocationDate": "toto"}], },
             "Checking revocationDate error message for revoked certificate in crlaction"),
        ]

        for data in data_test:
            with self.subTest(msg=data[1]):
                with self.assertRaises(ValidationError):
                    self._new_action(data[0])

    def test_check_no_dates(self):
        action = self._new_action({"sign_keyid": "key", "ca_id": "ca"})
        self.assertEqual(action.options.sign_keyid, 'key')
        self.assertEqual(action.options.ca_id, 'ca')

    def test_ceck_revoked_certs(self):
        action = self._new_action_success({
            "revokedCerts": [{"cert_id": "key", "revocationDate": "2020-07-06"}],
        })
        self.assertEqual(len(action.options.revokedCerts), 1)
        self.assertEqual(action.options.revokedCerts, [
            RevokedCerts(
                cert_id='key',
                revocationDate=datetime.datetime(2020, 7, 6, 0, 0, 0, 0)
            )
        ])

    @freeze_time("05-31-2014")
    def test_dates(self):
        data_test: List[Tuple[Dict, Dict, str]] = [
            (
                {},
                {
                    'offsetValidityTime': 0,
                    'offsetExpirationTime': 0,
                    'expirationTime': datetime.datetime(2014, 5, 31, 0, 0, 0, 0),
                    'validityTime': datetime.datetime(2014, 5, 31, 0, 0, 0, 0),
                },
                ""
            ),
            (
                {'offsetExpirationTime': 100,
                 'offsetValidityTime': 100, 'expirationTime': '2016-05-30'},
                {
                    'offsetExpirationTime': 100,
                    'offsetValidityTime': 100,
                    'expirationTime': datetime.datetime(2016, 5, 30, 0, 0, 0, 100000),
                    'validityTime': datetime.datetime(2014, 5, 31, 0, 0, 0, 100000),
                },
                ""
            ),
            (
                {'offsetExpirationTime': 100,
                 'offsetValidityTime': 200, 'validityTime': '2016-05-30'},
                {
                    'offsetExpirationTime': 100,
                    'offsetValidityTime': 200,
                    'expirationTime': datetime.datetime(2016, 5, 30, 0, 0, 0, 100000),
                    'validityTime': datetime.datetime(2016, 5, 30, 0, 0, 0, 200000),
                },
                ""
            ),
            (
                {'validityTime': '2016-05-31',
                 'expirationTime': '2016-05-30'},
                {
                    'offsetExpirationTime': 0,
                    'offsetValidityTime': 0,
                    'validityTime': datetime.datetime(2016, 5, 31, 0, 0, 0, 0),
                    'expirationTime': datetime.datetime(2016, 5, 30, 0, 0, 0, 0)
                },
                ""
            ),
            (
                {
                    "validityTime": "2019-05-12",
                    "expirationTime": "2018-05-12",
                    "offsetValidityTime": 10,
                    "offsetExpirationTime": 30
                },
                {
                    'offsetValidityTime': 10,
                    'offsetExpirationTime': 30,
                    'validityTime': datetime.datetime(2019, 5, 12, 0, 0, 0, 10000),
                    'expirationTime': datetime.datetime(2018, 5, 12, 0, 0, 0, 30000)
                },
                ""
            ),

        ]
        for data in data_test:
            with self.subTest(data[2]):
                action = self._new_action_success(data[0])
                self.assertEqual(action.options.offsetValidityTime,
                                 data[1]['offsetValidityTime'])
                self.assertEqual(action.options.offsetExpirationTime,
                                 data[1]['offsetExpirationTime'])
                self.assertEqual(action.options.validityTime,
                                 data[1]['validityTime'])
                self.assertEqual(action.options.expirationTime,
                                 data[1]['expirationTime'])
