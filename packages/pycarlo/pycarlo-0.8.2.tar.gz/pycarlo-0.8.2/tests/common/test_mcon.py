from unittest import TestCase
from uuid import UUID

from pycarlo.common import MCONParser


class MCONParserTests(TestCase):
    _TEST_ACCOUNT_ID = '12345678-1234-5678-1234-567812345678'
    _TEST_RESOURCE_ID = '21345678-1234-5678-1234-567812345678'
    _TEST_TABLE_ID = 'db:sch.tbl'

    def test_valid_table_mcon(self):
        mcon = f'MCON++{self._TEST_ACCOUNT_ID}++{self._TEST_RESOURCE_ID}++table++{self._TEST_TABLE_ID}'
        parsed_mcon = MCONParser.parse_mcon(mcon)
        self.assertIsNotNone(parsed_mcon)
        self.assertEqual(UUID(self._TEST_ACCOUNT_ID), parsed_mcon.account_id)
        self.assertEqual(UUID(self._TEST_RESOURCE_ID), parsed_mcon.resource_id)
        self.assertEqual('table', parsed_mcon.object_type)
        self.assertEqual(self._TEST_TABLE_ID, parsed_mcon.object_id)

    def test_invalid_mcon(self):
        mcon = 'invalid'
        parsed_mcon = MCONParser.parse_mcon(mcon)
        self.assertIsNone(parsed_mcon)

    def test_valid_field_mcon(self):
        field_id = f'{self._TEST_TABLE_ID}+++field_id'
        mcon = f'MCON++{self._TEST_ACCOUNT_ID}++{self._TEST_RESOURCE_ID}++field++{field_id}'
        parsed_mcon = MCONParser.parse_mcon(mcon)
        self.assertIsNotNone(parsed_mcon)
        self.assertEqual(UUID(self._TEST_ACCOUNT_ID), parsed_mcon.account_id)
        self.assertEqual(UUID(self._TEST_RESOURCE_ID), parsed_mcon.resource_id)
        self.assertEqual('field', parsed_mcon.object_type)
        self.assertEqual(field_id, parsed_mcon.object_id)
