# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
"""Test MIB YANG mapping."""

import os
import unittest2 as unittest

from yangsuite.paths import set_base_path, get_path
from yscoverage.mappings import (
    MibYangWriter,
    process_import_data,
    show_mapping_data
)


class MockMIBYANGpath:
    def __init__(self):
        self.yobj = {
            'model': ''
        }

    @staticmethod
    def translate_oids(oids, *args, **kwargs):
        return oids

    def label_xpath_keys(self, xpaths, *args, **kwargs):
        return xpaths


class TestMappings(unittest.TestCase):
    """Tests for paw wrapper tool."""
    @classmethod
    def setUpClass(cls):
        """Function that will be automatically called before each test."""
        cls.testdir = os.path.join(os.path.dirname(__file__), 'data')
        cls.fixtures = os.path.join(os.path.dirname(__file__), 'fixtures')
        set_base_path(cls.testdir)
        cls.mappingsdir = get_path('mibyang_mappings_dir', user='test')
        cls.wsdir = os.path.join(cls.testdir, 'ws')
        cls.modelfile = os.path.join(cls.wsdir, 'modelfiles')
        cls.modelfile_num = 1

    @classmethod
    def tearDownClass(cls):
        delete_file = os.path.join(
            cls.mappingsdir,
            'iosxe.experimental.17.8.20211130.DELETE.csv'
        )
        save_file = os.path.join(
            cls.mappingsdir,
            'iosxe.experimental.17.8.20211130.SAVE.csv'
        )
        import_file = os.path.join(
            cls.mappingsdir,
            'iosxe.experimental.17.8.20211130.IMPORT.csv'
        )
        if os.path.isfile(delete_file):
            os.remove(delete_file)
        if os.path.isfile(save_file):
            os.remove(save_file)
        if os.path.isfile(import_file):
            os.remove(import_file)

    def test_get_mapping_data(self):
        """Test loading a mappings file"""
        mapfile = os.path.join(
            self.mappingsdir,
            'iosxe.experimental.17.8.20211130.csv'
        )
        myw = MibYangWriter.get(
            mapfile,
            'test'
        )
        data = myw.get_mapping_data(
            mapfile,
            translate_oids=MockMIBYANGpath.translate_oids
        )
        self.assertIsNotNone(data)
        mib_paths, yang_paths, mib_to_yang, model_xpath, _ = data

        # OID and XPath must exist
        self.assertTrue(
            [p for p in mib_paths if p['oid'] == '.iso.org.dod.internet.private.enterprises.9.10.91.1.2.1.0']  # noqa
        )
        self.assertTrue(
            [x for x in yang_paths if x['value'] == '/interfaces/interface/if-index']  # noqa
        )
        # There are no mappings in the file
        self.assertEqual(len(mib_to_yang.keys()), 146)
        self.assertEquals(len(mib_paths), 3271)
        self.assertEquals(len(yang_paths), 146)
        self.assertEquals(len(model_xpath), 12)

    def test_save_mapping_in_csv(self):
        """Save mapping in CSV spreadsheet."""
        def translate_oids(oids, *args, **kwargs):
            return oids

        # Get some data to test with
        mapfile = os.path.join(
            self.mappingsdir,
            'iosxe.experimental.17.8.20211130.csv'
        )
        myw = MibYangWriter.get(
            mapfile,
            'test'
        )
        data = myw.get_mapping_data(
            mapfile,
            translate_oids=MockMIBYANGpath.translate_oids
        )
        mib_paths, yang_paths, mib_to_yang, model_xpath, _ = data

        # Add a fake match
        mib_to_yang.update({
            '.iso.org.dod.internet.mgmt': {
                'label': '/aaa-data/aaa-radius-stats/auth-port',
                'value': '/aaa-data/aaa-radius-stats/auth-port',
                'model': 'fake-module',
                'id': 'fake-id'
            }
        })
        model_xpath[
            '/aaa-data/aaa-radius-stats/auth-port'
        ] = 'fake-module'
        mib_paths = [{
            'oid': '.iso.org.dod.internet.mgmt',
            'value': '.iso.org.dod.internet.mgmt'
        }] + mib_paths

        savefile = os.path.join(
            self.mappingsdir,
            'iosxe.experimental.17.8.20211130.SAVE.csv'
        )

        myw2 = MibYangWriter.get(
            savefile,
            'test',
            mib_paths,
            yang_paths,
            model_xpath,
        )
        myw2.save_mapping_in_csv(
            oid='.iso.org.dod.internet.mgmt',
            mib_to_yang_paths=mib_to_yang,
            mibyang_path=MockMIBYANGpath()
        )
        save_data = myw2.get_mapping_data(savefile, translate_oids=MockMIBYANGpath.translate_oids)
        mib_paths, yang_paths, mib_to_yang, model_xpath, _ = save_data

        self.assertEquals(len(mib_paths), 147)
        self.assertEquals(len(yang_paths), 147)

        self.assertEquals(
            mib_to_yang['.iso.org.dod.internet.mgmt']['label'],
            '/aaa-data/aaa-radius-stats/auth-port'
        )
        self.assertTrue(
            [p for p in mib_paths if p['value'] == '.iso.org.dod.internet.mgmt']  # noqa
        )

    def test_delete_mapping_in_csv(self):
        """Delete mapping in Excel spreadsheet."""
        mapfile = os.path.join(
            self.mappingsdir,
            'iosxe.experimental.17.8.20211130.csv'
        )
        myw = MibYangWriter.get(
            mapfile,
            'test'
        )
        data = myw.get_mapping_data(
            mapfile,
            translate_oids=MockMIBYANGpath.translate_oids
        )
        mib_paths, yang_paths, mib_to_yang, model_xpath, _ = data
        # Add a fake match
        mib_to_yang.update({
            '.iso.org.dod.internet.mgmt': '/aaa-data/aaa-radius-stats/auth-port'  # noqa
        })
        mib_paths = [{
            'oid': '.iso.org.dod.internet.mgmt',
            'value': '.iso.org.dod.internet.mgmt'
        }] + mib_paths

        model_xpath[
            '/aaa-data/aaa-radius-stats/auth-port'
        ] = 'fake-module'

        delfile = os.path.join(
            self.mappingsdir,
            'iosxe.experimental.17.8.20211130.DELETE.csv'
        )

        myw2 = MibYangWriter.get(
            delfile,
            'test',
            mib_paths,
            yang_paths,
            model_xpath
        )

        myw2.save_mapping_in_csv(
            oid='.iso.org.dod.internet.mgmt',
            mib_to_yang_paths=mib_to_yang,
            mibyang_path=MockMIBYANGpath()
        )
        myw2.delete_mapping_in_csv('.iso.org.dod.internet.mgmt')
        del_data = myw2.get_mapping_data(
            delfile,
            translate_oids=MockMIBYANGpath.translate_oids
        )
        mib_paths, yang_paths, mib_to_yang, model_xpath, _ = del_data
        self.assertEquals(len(mib_paths), 146)
        self.assertEquals(len(yang_paths), 146)
        # This xpath should be removed
        self.assertFalse(
            len(
                [y for y in yang_paths
                    if y['value'] == '/aaa-data/aaa-radius-stats/auth-port']
            ),
            0
        )
        self.assertNotIn(
            '/aaa-data/aaa-radius-stats/auth-port',
            mib_to_yang.values()
        )
        self.assertNotIn(
            '.iso.org.dod.internet.mgmt',
            mib_to_yang.keys()
        )

    def test_process_import_data_file_and_dict(self):
        """Test import spreadsheet."""
        # pass in an Excel spreadsheet read from file
        file_data = open(os.path.join(
            self.mappingsdir,
            'iosxe.experimental.17.8.20211130.csv'
        )).read()
        file_path = os.path.join(
            self.mappingsdir,
            'iosxe.experimental.17.8.20211130.IMPORT.csv'
        )
        process_import_data([file_data], file_path, 'test')
        self.assertTrue(os.path.isfile(file_path))

    def test_show_mapping_data(self):
        """Import mapping from a spreadsheet."""
        def translate_oids(oids, to_numeric=False):
            return oids

        mapfile = os.path.join(
            self.mappingsdir,
            'iosxe.experimental.17.8.20211130.csv'
        )
        mib_paths, yang_paths, mib_to_yang, model_xpath, _ = show_mapping_data(
            mapfile,
            'test',
            translate_oids=MockMIBYANGpath.translate_oids
        )
        self.assertEquals(len(mib_paths), 3271)
        self.assertEquals(len(yang_paths), 146)
        self.assertEquals(len(model_xpath), 12)
        self.assertEqual(len(mib_to_yang.keys()), 146)


if __name__ == "__main__":
    unittest.main()
