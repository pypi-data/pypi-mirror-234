# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
"""Unit test cases for yscoverage.dataset module."""

import os
import pandas as pd
import unittest2 as unittest
from django.test import TestCase
from yangsuite.paths import set_base_path
from yscoverage.dataset import (
    dataset_for_yangset,
    YSDataSet,
    ALL_COLUMNS
)

TESTDIR = os.path.join(os.path.dirname(__file__), 'data')


class TestProprietaryYSYangDataset(unittest.TestCase):
    """Test cases for yscoverage.dataset module non pandas format."""
    def setUp(self):
        set_base_path(TESTDIR)
        self.maxDiff = None

    def test_yangset_dataset_basic(self):
        """Test dataset_for_yangset."""
        dataset = dataset_for_yangset('test', 'ocif-alpha', 'ietf-interfaces')

        self.assertEqual(['xpath', 'module'], dataset['header'])
        self.assertEqual([
            ['/interfaces', 'ietf-interfaces'],
            ['/interfaces/interface', 'ietf-interfaces'],
            ['/interfaces/interface/name', 'ietf-interfaces'],
            ['/interfaces/interface/description', 'ietf-interfaces'],
            ['/interfaces/interface/type', 'ietf-interfaces'],
            ['/interfaces/interface/enabled', 'ietf-interfaces'],
            ['/interfaces/interface/link-up-down-trap-enable',
             'ietf-interfaces'],
            ['/interfaces-state', 'ietf-interfaces'],
            ['/interfaces-state/interface', 'ietf-interfaces'],
            ['/interfaces-state/interface/name', 'ietf-interfaces'],
            ['/interfaces-state/interface/type', 'ietf-interfaces'],
            ['/interfaces-state/interface/admin-status', 'ietf-interfaces'],
            ['/interfaces-state/interface/oper-status', 'ietf-interfaces'],
            ['/interfaces-state/interface/last-change', 'ietf-interfaces'],
            ['/interfaces-state/interface/if-index', 'ietf-interfaces'],
            ['/interfaces-state/interface/phys-address', 'ietf-interfaces'],
            ['/interfaces-state/interface/higher-layer-if', 'ietf-interfaces'],
            ['/interfaces-state/interface/lower-layer-if', 'ietf-interfaces'],
            ['/interfaces-state/interface/speed', 'ietf-interfaces'],
            ['/interfaces-state/interface/statistics', 'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/discontinuity-time',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/in-octets',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/in-unicast-pkts',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/in-broadcast-pkts',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/in-multicast-pkts',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/in-discards',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/in-errors',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/in-unknown-protos',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/out-octets',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/out-unicast-pkts',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/out-broadcast-pkts',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/out-multicast-pkts',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/out-discards',
             'ietf-interfaces'],
            ['/interfaces-state/interface/statistics/out-errors',
             'ietf-interfaces'],
        ], dataset['data'])

    def test_yangset_dataset_addons(self):
        """Test dataset_for_yangset with addons."""
        dataset = dataset_for_yangset('test', 'ocif-alpha', 'ietf-interfaces',
                                      ['nodetype', 'datatype'])

        self.assertEqual(['xpath', 'module', 'nodetype', 'datatype'],
                         dataset['header'])
        self.assertEqual([
            ['/interfaces', 'ietf-interfaces', 'container', ''],
            ['/interfaces/interface', 'ietf-interfaces', 'list', ''],
            ['/interfaces/interface/name',
             'ietf-interfaces', 'leaf', 'string'],
            ['/interfaces/interface/description',
             'ietf-interfaces', 'leaf', 'string'],
            ['/interfaces/interface/type',
             'ietf-interfaces', 'leaf', 'identityref'],
            ['/interfaces/interface/enabled',
             'ietf-interfaces', 'leaf', 'boolean'],
            ['/interfaces/interface/link-up-down-trap-enable',
             'ietf-interfaces', 'leaf', 'enumeration'],
            ['/interfaces-state', 'ietf-interfaces', 'container', ''],
            ['/interfaces-state/interface', 'ietf-interfaces', 'list', ''],
            ['/interfaces-state/interface/name',
             'ietf-interfaces', 'leaf', 'string'],
            ['/interfaces-state/interface/type',
             'ietf-interfaces', 'leaf', 'identityref'],
            ['/interfaces-state/interface/admin-status',
             'ietf-interfaces', 'leaf', 'enumeration'],
            ['/interfaces-state/interface/oper-status',
             'ietf-interfaces', 'leaf', 'enumeration'],
            ['/interfaces-state/interface/last-change',
             'ietf-interfaces', 'leaf', 'yang:date-and-time'],
            ['/interfaces-state/interface/if-index',
             'ietf-interfaces',  'leaf', 'int32'],
            ['/interfaces-state/interface/phys-address',
             'ietf-interfaces', 'leaf', 'yang:phys-address'],
            ['/interfaces-state/interface/higher-layer-if',
             'ietf-interfaces',
             'leaf-list',
             'interface-state-ref'],
            ['/interfaces-state/interface/lower-layer-if',
             'ietf-interfaces',
             'leaf-list',
             'interface-state-ref'],
            ['/interfaces-state/interface/speed',
             'ietf-interfaces', 'leaf', 'yang:gauge64'],
            ['/interfaces-state/interface/statistics',
             'ietf-interfaces', 'container', ''],
            ['/interfaces-state/interface/statistics/discontinuity-time',
             'ietf-interfaces',
             'leaf',
             'yang:date-and-time'],
            ['/interfaces-state/interface/statistics/in-octets',
             'ietf-interfaces',
             'leaf',
             'yang:counter64'],
            ['/interfaces-state/interface/statistics/in-unicast-pkts',
             'ietf-interfaces',
             'leaf',
             'yang:counter64'],
            ['/interfaces-state/interface/statistics/in-broadcast-pkts',
             'ietf-interfaces',
             'leaf',
             'yang:counter64'],
            ['/interfaces-state/interface/statistics/in-multicast-pkts',
             'ietf-interfaces',
             'leaf',
             'yang:counter64'],
            ['/interfaces-state/interface/statistics/in-discards',
             'ietf-interfaces',
             'leaf',
             'yang:counter32'],
            ['/interfaces-state/interface/statistics/in-errors',
             'ietf-interfaces',
             'leaf',
             'yang:counter32'],
            ['/interfaces-state/interface/statistics/in-unknown-protos',
             'ietf-interfaces',
             'leaf',
             'yang:counter32'],
            ['/interfaces-state/interface/statistics/out-octets',
             'ietf-interfaces',
             'leaf',
             'yang:counter64'],
            ['/interfaces-state/interface/statistics/out-unicast-pkts',
             'ietf-interfaces',
             'leaf',
             'yang:counter64'],
            ['/interfaces-state/interface/statistics/out-broadcast-pkts',
             'ietf-interfaces',
             'leaf',
             'yang:counter64'],
            ['/interfaces-state/interface/statistics/out-multicast-pkts',
             'ietf-interfaces',
             'leaf',
             'yang:counter64'],
            ['/interfaces-state/interface/statistics/out-discards',
             'ietf-interfaces',
             'leaf',
             'yang:counter32'],
            ['/interfaces-state/interface/statistics/out-errors',
             'ietf-interfaces',
             'leaf',
             'yang:counter32']
        ], dataset['data'])


class TestPandasYSDataSet(TestCase):
    """Test cases for YSDataSet class pandas.DataFrame format."""
    # django TestCase used here.

    @classmethod
    def setUpTestData(cls):
        set_base_path(TESTDIR)
        cls.maxDiff = None

    def test_get_dataset_tree_from_directory(self):
        """Test get tree from directory."""
        ysds = YSDataSet(yang_dir=os.path.join(TESTDIR, 'yang', 'version1'))
        data = ysds.get_tree_from_directory(modules=['openconfig-interfaces'])
        tree = data[0]

        self.assertEqual(tree['text'], 'openconfig-interfaces')
        self.assertEqual(tree['children'][0]['text'], 'interfaces')
        self.assertEqual(tree['children'][0]['children'][0]['text'],
                         'interface')
        self.assertEqual(tree['children'][0]['children'][0]['children'][0]
                         ['text'], 'name')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['text'], 'config')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['children'][0]['text'], 'name')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['children'][1]['text'], 'type')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['children'][2]['text'], 'mtu')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['children'][3]['text'], 'loopback-mode')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['children'][4]['text'], 'description')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['text'], 'state')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['children'][0]['text'], 'name')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['children'][1]['text'], 'type')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['children'][2]['text'], 'mtu')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['children'][3]['text'], 'loopback-mode')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['children'][4]['text'], 'description')
        # Thats pretty good so stop here.

    def test_get_dataset_tree_from_database(self):
        """Test get tree from database."""
        ysds = YSDataSet(owner='test', setname='ocif-beta',)
        data = ysds.get_dataset_trees(modules=['openconfig-interfaces'])
        tree = data[0]

        self.assertEqual(tree['text'], 'openconfig-interfaces')
        self.assertEqual(tree['children'][0]['text'], 'interfaces')
        self.assertEqual(tree['children'][0]['children'][0]['text'],
                         'interface')
        self.assertEqual(tree['children'][0]['children'][0]['children'][0]
                         ['text'], 'name')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['text'], 'config')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['children'][0]['text'], 'name')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['children'][1]['text'], 'type')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['children'][2]['text'], 'mtu')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['children'][3]['text'], 'loopback-mode')
        self.assertEqual(tree['children'][0]['children'][0]['children'][1]
                         ['children'][4]['text'], 'description')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['text'], 'state')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['children'][0]['text'], 'name')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['children'][1]['text'], 'type')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['children'][2]['text'], 'mtu')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['children'][3]['text'], 'loopback-mode')
        self.assertEqual(tree['children'][0]['children'][0]['children'][2]
                         ['children'][4]['text'], 'description')
        # Thats pretty good so stop here.

    def test_get_pandas_dataframe_from_dict(self):
        """Given a jstree, create a pandas.DataFrame."""
        ysds = YSDataSet(yang_dir=os.path.join(TESTDIR, 'yang', 'version1'))
        data = ysds.get_tree_from_directory(modules=['openconfig-interfaces'])
        tree = data[0]
        df_list = ysds.get_pandas_df(tree, [])
        df = pd.DataFrame(df_list, columns=ALL_COLUMNS)

        self.assertEqual(df.shape, (78, 33))
        self.assertEqual(df.columns.tolist(), ALL_COLUMNS)

        mtu = df.loc[df['xpath'] == '/interfaces/interface/config/mtu']
        self.assertEqual(mtu['nodetype'].values[0], 'leaf')
        self.assertEqual(mtu['datatype'].values[0], 'uint16')
        self.assertEqual(mtu['module'].values[0], 'openconfig-interfaces')
        self.assertEqual(mtu['xpath'].values[0],
                         '/interfaces/interface/config/mtu')
        # Thats pretty good so stop here.

    def test_pandas_dataset(self):
        """Using YSDataSet class, create a pandas.DataFrame."""
        ysds = YSDataSet(yang_dir=os.path.join(TESTDIR, 'yang', 'version1'))
        ysds.dataset_for_pandas(modules=['openconfig-interfaces'])
        df = ysds.dfs['openconfig-interfaces']

        self.assertEqual(df.shape, (78, 33))
        self.assertEqual(df.columns.tolist(), ALL_COLUMNS)

        mtu = df.loc[df['xpath'] == '/interfaces/interface/config/mtu']
        self.assertEqual(mtu['nodetype'].values[0], 'leaf')
        self.assertEqual(mtu['datatype'].values[0], 'uint16')
        self.assertEqual(mtu['module'].values[0], 'openconfig-interfaces')
        self.assertEqual(mtu['xpath'].values[0],
                         '/interfaces/interface/config/mtu')
        # Thats pretty good so stop here.

    def test_pandas_diffset(self):
        """Test pandas compare of yangsets."""
        ALL_COLUMNS.remove('revision')
        ysds = YSDataSet(yang_dir=os.path.join(TESTDIR, 'yang', 'version1'))
        ysds.dataset_for_pandas(
            modules=['openconfig-interfaces'], columns=ALL_COLUMNS
        )
        ysds2 = YSDataSet(yang_dir=os.path.join(TESTDIR, 'yang', 'version2'))
        ysds2.dataset_for_pandas(
            modules=['openconfig-interfaces'], columns=ALL_COLUMNS
        )
        ysds.dataset_model_diff(ysds2)

        self.assertEqual(ysds.dfs['openconfig-interfaces'].shape, (78, 32))
        self.assertIn('openconfig-interfaces', ysds.df_diffs)
        self.assertIn('diff', ysds.df_diffs['openconfig-interfaces'])
        self.assertIn('new', ysds.df_diffs['openconfig-interfaces'])
        self.assertIn('removed', ysds.df_diffs['openconfig-interfaces'])
        self.assertEqual(ysds.df_diffs['openconfig-interfaces']['diff'].shape,
                         (94, 9))
        self.assertEqual(ysds.df_diffs['openconfig-interfaces']['new'].shape,
                         (1, 32))
        self.assertEqual(ysds.df_diffs['openconfig-interfaces']['removed'].shape,
                         (6, 32))

        diff = pd.read_csv(
            os.path.join(TESTDIR, 'csvs', 'diff.csv'), keep_default_na=False
        )
        self.assertTrue(
            all(
                diff.xpath.values == ysds.df_diffs['openconfig-interfaces']['diff'].xpath.values  # noqa
            )
        )
        new = pd.read_csv(
            os.path.join(TESTDIR, 'csvs', 'new.csv'), keep_default_na=False
        )
        self.assertTrue(
            all(
                new.xpath.values == ysds.df_diffs['openconfig-interfaces']['new'].xpath.values  # noqa
            )
        )
        removed = pd.read_csv(
            os.path.join(TESTDIR, 'csvs', 'removed.csv'), keep_default_na=False
        )
        self.assertTrue(
            all(
                removed.xpath.values == ysds.df_diffs['openconfig-interfaces']['removed'].xpath.values  # noqa
            )
        )
