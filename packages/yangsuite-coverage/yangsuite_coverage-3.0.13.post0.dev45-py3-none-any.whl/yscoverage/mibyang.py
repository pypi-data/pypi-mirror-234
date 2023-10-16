#! /usr/bin/env python
# Copyright 2021 Cisco Systems Inc, All rights reserved.
import os
import subprocess
import re
import json
import traceback
from lxml import etree as ET
from elasticsearch import Elasticsearch, helpers
from pathlib import PosixPath
from collections import OrderedDict

from yangsuite import get_logger
from yangsuite.paths import get_path
from ysfilemanager import split_user_set
from yscoverage.dataset import dataset_for_yangset, dataset_for_directory
from ysnetconf.nconf import SessionKey, ncclient_send
from yscoverage.mappings import MibYangWriter
from ysyangtree import YSContext, YSYangModels
from ysyangtree.ymodels import TreeWalker


log = get_logger(__name__)


class YANGpathException(Exception):
    pass


class MIBpathException(Exception):
    pass


class MIBpath:
    """Given a MIB, construct 3 styles of OID path lists.

    1. Human readable dot separated.
      - Split into a dataset used to compare with YANG Xpath.
      - Can be used to query device.
    2. Human readable plus OID number dot separated.
      - Display for user which gives both styles for easy reference
    3. OID.
      - Can be used to query device.
    """
    CAMELCASE_SPLIT_RE = re.compile(
        '.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)'
    )

    def __init__(self, mib, logger=None):
        self.mib = mib
        self.readable = []
        if logger is not None:
            self.log = logger
        else:
            self.log = log

    @property
    def mib(self):
        return self._mib

    @mib.setter
    def mib(self, mib_or_file):
        if os.path.isfile(mib_or_file):
            self._path = os.path.dirname(mib_or_file)
            self._mib = os.path.basename(mib_or_file).replace('.my', '')
        else:
            self._mib = 'None'
            self._path = 'None'

    def read_mib(self, cmd, mib):
        """Using snmp library, return request MIB data.

        Args:
            cmd (list): List of bash shell commands.
            mib (str): MIB file path.
        Returns:
            buffer containing MIB file content.
        """
        BUFSIZE = 8192

        p = subprocess.Popen(cmd, bufsize=BUFSIZE,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             universal_newlines=True)

        buf = ''
        while True:
            data = p.stdout.read(1)
            if not data:
                if not buf:
                    self.log.error('No data received from MIB')
                p.terminate()
                break

            buf += data

        return buf

    def camel_case_split(self, identifier):
        matches = re.finditer(self.CAMELCASE_SPLIT_RE, identifier)
        return [m.group(0).lower() for m in matches]

    def get_readable(self):
        """Construct the human readable list of OID."""
        if not os.path.isfile(os.path.join(self._path, self.mib) + '.my'):
            self.log.warning('MIB file not found {0}'.format(self.mib))
            # Give snmpwalk a place to start
            self.readable.append('.iso.org.dod.internet')
            return
        # Get human readable form and OIDs
        cmd = ['snmptranslate', '-m', self.mib, '-M', self._path, '-Tos']
        try:
            data = self.read_mib(cmd, self.mib)
        except FileNotFoundError:
            self.log.warning('snmptranslate not found')
            # Give snmpwalk a place to start
            self.readable.append('.iso.org.dod.internet')
            return
        self.oids = []

        df_prep = {}

        for line in data.splitlines():
            if line.startswith('.1.3.6.1'):
                oid = line
            elif line.startswith('.iso.org.dod.internet'):
                mpath = line
                self.readable.append(line)
                tokens = []
                split_path = mpath.split('.')
                for seg in split_path:
                    if seg in ['iso', 'org', 'dod', 'internet', 'mgmt',
                               'mib-2', 'snmpV2', 'snmp']:
                        continue
                    tokens += self.camel_case_split(seg)
                if tokens:
                    ' '.join(set(tokens)),
                    tokens.reverse()
                df_prep[mpath] = {
                    'tokens': tokens,
                    'mpath': mpath,
                    'oid': oid,
                    'value': None
                }

        self.mib_df = df_prep


class YANGpath:
    """Given a YANG model, create a dataset of all xpaths."""

    def __init__(self, model, yangset=None, addons=None):
        self.yangset = yangset
        self.model = model
        self.xpaths = []
        if addons is None:
            self.addons = ['nodetype', 'presence', 'namespace']
        else:
            # TODO: what if addons is not None?
            self.addons = addons

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model_or_file):
        if os.path.isfile(model_or_file):
            self._path = os.path.dirname(model_or_file)
            self._model = os.path.basename(model_or_file)
            if '@' in self._model:
                self._model = self._model[:self._model.find('@')]
            else:
                self._model = self._model.replace('.yang', '')
        else:
            self._model = model_or_file

    def get_readable(self):
        """Create dataset of model and convert to pandas Dataframe."""
        if self.yangset:
            owner, setname = split_user_set(self.yangset)
            dataset = dataset_for_yangset(
                owner, setname, self.model, self.addons
            )
        elif hasattr(self, '_path'):
            # dataset is dict:
            # {"header": list for top of spreadsheet,
            #  "data": list (row basically) of lists}
            # TODO: should have API returning a pandas.DataFrame
            dataset = dataset_for_directory(
                self._path, self.model, self.addons
            )
        else:
            log.error('Invalid model file path.')
            raise YANGpathException('Invalid model file path.')

        df_prep = {}
        root_namespace = None
        headers = {}
        for i, h in enumerate(dataset['header']):
            # get index of headers to work with lists in list
            headers[h] = i

        for data in dataset['data']:
            if data[headers['nodetype']] in ['leaf', 'leaflist'] or \
                    data[headers['presence']]:
                # Only want Xpaths pointing to significant data.
                xpath = data[headers['xpath']]
                # list of xpath segments
                tokens = []
                namespaceless_xpath = ''
                for seg in xpath.split('/'):
                    if seg:
                        tokens += seg.split('-')
                        # Remove namespace from seg
                        if ':' in seg:
                            namespaceless_xpath += f'/{seg.split(":")[-1]}'
                        else:
                            namespaceless_xpath += f'/{seg}'
                # Create a list of XPaths present in the current model
                self.xpaths.append(namespaceless_xpath)
                df_prep[namespaceless_xpath] = {
                    'tokens': tokens,
                    'namespace': data[headers['namespace']]
                }
                if root_namespace is None:
                    df_prep['root_namespace'] = data[headers['namespace']]
                    root_namespace = data[headers['namespace']]

        self.yang_df = df_prep


class MIBYANGpath:
    """Operations matching a MIBpath object to a YANGpath object."""

    mypath = {}
    XP_KEY = '[key=value]'
    OID_KEY = '<>'

    def __init__(
        self, model, user, device, yangset=None,
        map_filename='', starting_oids=[],
        model_revision=''
    ):
        self.yangset = yangset
        self.yobj = model
        self.yobj_revision = model_revision
        self.device = device
        self.host = self.device.base.profile_name
        self.address = self.device.base.address
        self.device_user = self.device.base.username
        self.device_password = self.device.base.password
        self.user = user
        walk_filename = self.get_filename()
        # Translate starting OIDs for comparison with walk file later
        self.starting_oids = self.translate_oids(starting_oids)

        if hasattr(self.yobj, '_path'):
            walk_path = os.path.dirname(self.yobj._path)
        else:
            walk_path = get_path('mibyang_mappings_dir', user=self.user)
        # Get values to OIDs and filepath from walk file
        self.oids_to_values, self.walk_file = self.load_walk_file(
            walk_path, walk_filename
        )
        # If mapping filepath is provided, use it, otherwise use generated path
        self.map_filepath = ''
        if map_filename:
            self.map_filepath = os.path.join(
                get_path('mibyang_mappings_dir', user=self.user),
                map_filename
            )
        else:
            self.map_filepath = self.walk_file.replace('.walk', '.csv')
        if os.path.isfile(self.map_filepath):
            self.mapped_df = MibYangWriter.read_map_file(self.map_filepath)
        else:
            self.mapped_df = None

        self.xpaths_to_values = {}
        # TreeWalker is used to get node data for any XPath
        self.tree_walkers = {}
        self.modules_to_matched_xpaths = {}
        self.es = Elasticsearch()

    @classmethod
    def get(
        self, model, user, device=None, yangset=None,
        map_filename='', starting_oids='', model_revision=''
    ):
        if starting_oids:
            # Transform starting oids from URI query str to list format
            starting_oids = [
                token.strip()
                for token in starting_oids.split(',')
            ]
        mypobj = self.mypath.get((model, user), None)
        if (mypobj is None and device is not None) \
           or (
               mypobj is not None
               and device is not None
               and mypobj.starting_oids != mypobj.translate_oids(starting_oids)):
            mypobj = self(
                model, user, device,
                yangset, map_filename=map_filename,
                starting_oids=starting_oids,
                model_revision=model_revision
            )
            self.mypath[(model, user)] = mypobj
        elif mypobj is not None and map_filename:
            # Add user selected mapfile path if there is any
            mypobj.map_filename = map_filename
            mypobj.map_filepath = os.path.join(
                get_path('mibyang_mappings_dir', user=self.user),
                map_filename
            )
        return mypobj

    @classmethod
    def force_walk(self, model, user):
        mypobj = self.mypath.get((model, user), None)
        if mypobj:
            mypobj.oids_to_values = {}

    @property
    def yobj(self):
        return self._yobj

    @yobj.setter
    def yobj(self, model):
        if self.yangset:
            self._yobj = YANGpath(model, self.yangset)
        else:
            self._yobj = YANGpath(model)
        self._yobj.get_readable()

    RE_VERSION = re.compile('\d+\.\d+\.\d+')  # noqa: W605

    @staticmethod
    def load_walk_file(walk_filepath, walk_filename):
        """Load walk files if same major
           version & minor version is equal or higher.

        Args:
            walk_path (str): path that holds the walk file
            walk_file (str): target walk filename

        Returns:
            oids_to_values (dict): dict mapping between OIDs to device values.
            curr_file_path (str): abs. path to walk file
        """
        oids_to_values = {}
        curr_walk_filename = walk_filename
        # Append file ext. if none exists
        if not curr_walk_filename.endswith('.walk'):
            curr_walk_filename = f'{curr_walk_filename}.walk'
        # Get version numbers tokens from walk file
        dot_tokens = [
            token for token in curr_walk_filename.split('.') if token
        ]
        if len(dot_tokens) < 4:
            # Invalid walk file length
            log.error(
                'Invalid filename. Please prepend device OS name '
                + 'followed by a dot ("iosxe." or "iosxr." or "nxos.") for '
                + f'file: {os.path.join(walk_filepath, curr_walk_filename)}'
            )
            raise ValueError(
                'Invalid filename. Please prepend device OS name '
                + 'followed by a dot ("iosxe." or "iosxr." or "nxos.") for '
                + f'file: {os.path.join(walk_filepath, curr_walk_filename)}'
            )
        # Get OS from walk file
        orig_os = dot_tokens[0]
        # Get major and minor versions from walk filename
        orig_major, orig_minor = dot_tokens[-4:-2]
        curr_minor = orig_minor

        # Walk thru all .walk files in directory
        path = PosixPath(walk_filepath)
        for file in path.glob('*.walk'):
            file_path = file.__str__()
            filename = file_path.split('/')[-1]
            file_dot_tokens = [token for token in filename.split('.') if token]
            if not file_dot_tokens \
               or not (
                   len(file_dot_tokens) == 5
                   or len(file_dot_tokens) == 6
               ):
                # Invalid filename
                log.error(
                    'Invalid filename. Please prepend device OS name '
                    + 'followed by a dot ("iosxe." or "iosxr." or "nxos.") '
                    + f'for file: {file_path}'
                )
                continue
            # Get OS from filename
            file_os = file_dot_tokens[0]
            # Get major and minor versions from filename
            major, minor = file_dot_tokens[-4:-2]
            if (
                file_os == orig_os
                and int(major) == int(orig_major)
                and int(minor) == int(orig_minor)
            ):
                # Stop finding walk files because exact match has been found
                curr_walk_filename = filename
                break
            elif (
                file_os == orig_os
                and int(major) == int(orig_major)
                and int(minor) > int(curr_minor)
            ):
                # Replace the curr. walk file
                # New .walk file has higher minor ver. num.
                curr_walk_filename = filename
                curr_minor = minor

        curr_filepath = os.path.join(walk_filepath, curr_walk_filename)
        if (
            # Check if file exists and not empty
            os.path.isfile(curr_filepath)
            and os.stat(curr_filepath).st_size > 0
        ):
            # Load values to OIDs mappings from file
            file = open(curr_filepath)
            oids_to_values = json.load(file)
            file.close()

        return (oids_to_values, curr_filepath)

    @staticmethod
    def translate_oids(oids, to_numeric=False):
        '''Translate OIDs to human-readable in-place for list/dict arg'''
        try:
            # Get argument type
            if not isinstance(oids, (list, dict)) \
               or not oids:
                return oids
            translated = []
            untranslated = oids
            if isinstance(oids, dict):
                # Arg type is list by default, if dict return dict
                translated = {}
                untranslated = list(oids.keys())

            for index in range(len(untranslated)):
                tgt_oid = untranslated[index]
                translated_oid = tgt_oid
                oid_has_keys = False

                # Remove keys from OID
                if MIBYANGpath.OID_KEY in tgt_oid:
                    tgt_oid = tgt_oid.replace(f'.{MIBYANGpath.OID_KEY}', '')
                    oid_has_keys = True
                cmd = [
                    'snmptranslate',
                    '-M', get_path('mibs_dir'),
                    '-m', 'ALL',
                    '-Pu',
                    '-Tso',
                    '-On'if to_numeric
                    else '-Of',
                    tgt_oid
                ]
                # Run translate cmd
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                out, _ = process.communicate()
                if out:
                    out = out.decode('utf-8', errors='replace')
                    # Translated OID should be at the end of output
                    translated_oid = out.splitlines()[-1].strip()
                    if oid_has_keys:
                        translated_oid = f'{translated_oid}.{MIBYANGpath.OID_KEY}'
                # Kill process
                process.terminate()

                if isinstance(oids, list):
                    translated.append(translated_oid)
                elif isinstance(oids, dict):
                    if oid_has_keys:
                        # The original key in oids arg has key, so add key back in
                        tgt_oid = f'{tgt_oid}.{MIBYANGpath.OID_KEY}'
                    translated[translated_oid] = oids[tgt_oid]
        except KeyError as e:
            log.error(f'Unable to find key: {e}')
        return translated

    def get_filename(self):
        """Standard file name is based on IOS version."""
        _, version = self.get_oids_to_values_from_device(
            'snmpget',
            options=['.1.3.6.1.2.1.1.1.0'],
            translate_oids=False
        )
        if not version:
            log.error('Unable to get device version. No response from device.')
            raise ValueError('Unable to get device version. No response from device.')

        prefix = ''
        if 'NXOS' in version:
            prefix = 'nxos.'
        elif 'IOSXE' in version:
            prefix = 'iosxe.'
        elif 'IOS' in version and 'XR' in version:
            prefix = 'iosxr.'
        if 'Experimental' in version:
            prefix += 'experimental.'
        major_minor = re.findall(self.RE_VERSION, version)
        if major_minor:
            if not prefix or prefix == 'experimental.':
                # Unable to get OS from device
                base = self.device.dict()['base']
                device_name = base['profile_name'].strip().replace('.', '')
                # Append device name to filename
                prefix = f'{device_name}.{prefix}'
            return prefix + major_minor[0]
        else:
            log.error('Unable to determine image version.')
            raise ValueError('Unable to determine image version.')

    def _es_generator(self, df):
        for i, mpath_row in enumerate(df.items()):
            mpath, df_row = mpath_row
            yield {
                # "_index": self.mobj.mib.lower(),
                "_id": i,
                "_source": {
                    "mpath": mpath,
                    "tokens": df_row['tokens'],
                    "oid": df_row['oid']
                }
            }

    def populate_elasticsearch(self, df):
        """Populate elasticsearch with pandas.DataFrame.

        Args:
          df (pandas.DataFrame): source could be from MIB or YANG.
        Return:
          tuple - population results
        """

        # Create and populate index
        return helpers.bulk(self.es, self._es_generator(df))

    def _clear_elasticsearch(self):
        # Clear previous indexes from Elasticsearch
        res = self.es.indices.get(index='*')
        if isinstance(res, dict):
            for col in res.keys():
                if self.es.indices.exists(col):
                    self.es.indices.delete(col)

    def _fuzzymatch_one(self, index, segment):
        hits = []
        matches = {}
        score = 0.0
        for seg in set(segment):
            res = self.es.search(
                index=index,
                body={
                    "query": {
                        "fuzzy": {
                            "tokens": {
                                "value": seg
                            }
                        }
                    }
                }
            )
            if 'hits' in res:
                hits += res['hits']['hits']
        if hits:
            for h in hits:
                if h['_source']['mpath'] in matches:
                    matches[h['_source']['mpath']] += 1
                else:
                    matches[h['_source']['mpath']] = 1
            high_score = max(set(matches.values()))
            if [m for m in matches.values()].count(high_score) == 1:
                for mpath, score in matches.items():
                    if high_score == score:
                        return (mpath, high_score)
        return (None, 0)

    def fuzzymatch(self, df_source=None, df_dest=None):
        """Attempt to fuzzy match MIBpath and YANGpath segments.

        Args:
          df_source (pandas.DataFrame): Fuzzy match to df_dest
          df_dest (pandas.DataFrame): Input to Elasticsearch for fuzzy matches.
        """
        if df_source is None:
            df_source = self.yobj.yang_df
        # if df_dest is None:
        #     df_dest = self.mobj.mib_df

        # Reset search criteria
        self._clear_elasticsearch()

        # Elasticsearch will perform fuzzy matching on destination.
        success, errors = self.populate_elasticsearch(df_dest)
        if errors:
            log.error('Elasticsearch Index errors:\n{0}'.format(errors))

        if success:
            log.info('Elasticsearch successful entries: {0}'.format(success))
            res = self.es.indices.get(index='*')
            if isinstance(res, dict):
                for indice in res.keys():
                    for xpath, segments in df_source.items():
                        if 'tokens' not in segments:
                            continue
                        mpath, score = self._fuzzymatch_one(
                            indice, segments['tokens']
                        )
                        if mpath and score:
                            print('score:{0}\nxpath:{1}\nmpath{2}'.format(
                                score, xpath, mpath
                            ))
                # highest score here, might be a match
                # get mib and yang path to assoc. them
                # if no assoc. no value in pulldown
    """ space separate mib path and yang xpaths
        turn both into sentences with a value at the
        end and use elasticsearch"""

    year_rx = re.compile(
        r'(([0-9]{4}-[0-9]{2}-[0-9]{2})|([0-9]{2}-[0-9]{2}-[0-9]{4}))'
    )
    time_rx = re.compile(r'([0-9]{2}:[0-9]{2}:[0-9]{2})')

    def oids_to_xpaths_map(self, oids_to_values, xpaths_to_values):
        """Given two mapping dicts: OIDs to values and XPaths to values,
        loop through each OID value and find intersection in XPaths to values

        Args:
            oids_to_values (dict): mapping of OIDs to set device values
            xpaths_to_values (dict): mapping of XPaths to set device values

        Returns:
            dict: compacted mapping of OIDs to XPaths
        """
        # staticmethod makes it easier to debug.
        oids_to_xpaths = {}
        # Match OID values to XPaths
        for oid, oid_value in oids_to_values.items():
            matched_xpath_val = False
            for xp, vals in xpaths_to_values.items():
                if oid_value in vals:
                    self.modules_to_matched_xpaths[xp] = self.yobj.model
                    if oid in oids_to_xpaths:
                        oids_to_xpaths[oid].append(xp)
                    else:
                        oids_to_xpaths[oid] = [xp]
                    matched_xpath_val = True
            if not matched_xpath_val:
                oids_to_xpaths[oid] = []
        return oids_to_xpaths

    def bubble_up_values(self, target_dict):
        """For any dict, return OrderedDict with all keys with values
           shifted to the front"""
        with_values = {}
        no_values = {}

        for key in target_dict:
            if target_dict[key]:
                with_values[key] = target_dict[key]
            else:
                no_values[key]
        result = OrderedDict({**with_values, **no_values})

        return result

    def get_oids_not_in_subtree(self, oids_list, target_list):
        """Get list of OIDs not part of subtree in target list"""

        def prefix_in_list(prefix, target_list):
            """Returns a boolean for finding str prefix in a list of str"""
            for elem in target_list:
                if elem.startswith(prefix):
                    return True
            return False

        if not target_list:
            return oids_list

        result = []
        for oid in oids_list:
            if not prefix_in_list(oid, target_list):
                result.append(oid)
        return result

    def get_device_oids_to_xpaths_map(self, get_from_device=True):
        '''Try to match OID values and Xpath values.'''
        # Find if starting OID is already in OIDs to values
        # TODO: move force walk check and processing over here
        # TODO: write updated sanity tests
        target_oids = self.get_oids_not_in_subtree(
            self.starting_oids, list(self.oids_to_values.keys())
        )
        target_oids_to_values = {}
        # Do new walk to get target OIDs or get OIDs that were prev. walked
        if ((
            # No snmpwalk has been performed on this device yet
            not self.oids_to_values
            # No intersection between starting OIDs and walked OIDs
            or target_oids) and get_from_device
        ):  # noqa: E124
            # Do snmpwalk on starting OID(s) not present in OIDs to values
            target_oids_to_values, _ = self.get_oids_to_values_from_device(
                'snmpwalk',
                options=target_oids
            )
            if not target_oids_to_values:
                log.error(
                    'Device doesn\'t have OID(s) to start matching from.'
                )
                raise ValueError(
                    'Device doesn\'t have OID(s) to start matching from.'
                )

            # Append new values to mapping dict and save to walk file
            self.oids_to_values = self.translate_oids({
                **self.oids_to_values, **target_oids_to_values
            })
            json.dump(self.oids_to_values, open(self.walk_file, 'w+'))
        elif self.oids_to_values:
            # Starting OID already in walk file, retrieve & send to frontend
            for mapped in list(self.oids_to_values.keys()):
                for oid in self.starting_oids:
                    if mapped.startswith(oid):
                        target_oids_to_values[mapped] = self.oids_to_values[
                            mapped
                        ]
        self.xpaths_to_values = self.get_xpaths_to_values_from_device()
        # If user specified starting OIDs, map the starting OIDs only
        oids_to_xpaths = self.oids_to_xpaths_map(
            target_oids_to_values or self.oids_to_values,
            self.xpaths_to_values
        )

        # Refresh cached mapped Dataframe, in case user has prev. saved mapping
        if os.path.isfile(self.map_filepath):
            self.mapped_df = MibYangWriter.read_map_file(self.map_filepath)
        if self.mapped_df is not None:
            for irow in self.mapped_df.iterrows():
                row = irow[1].to_dict()
                if row['YANG Xpath']:
                    if row['OID'] in oids_to_xpaths:
                        oids_to_xpaths[row['OID']] += [row['YANG Xpath']]
                    elif row['OID'] not in oids_to_xpaths:
                        oids_to_xpaths[row['OID']] = [row['YANG Xpath']]
        # Translate OIDs to standardize OIDs to be human-readable only
        oids_to_xpaths = self.label_oid_keys(self.translate_oids(oids_to_xpaths))
        return oids_to_xpaths

    def label_xpath_keys(self, xpaths_obj):
        """Place [key=value] string where the XPath includes
        a list element.
        Ex. /native/interface/GigabitEthernet/name ->
        /native/interface/GigabitEthernet[key=value]/name

        Args:
            xpaths_dict (dict/list): A dict or list with XPaths as keys

        Returns:
            (dict): Modified dict from arg with certain keys labeled
            with key indexes
        """
        # TODO: write sanity tests
        def create_tree_walkers():
            """Create tree walker instances to get node data of XPath"""
            tree_walkers = []
            owner, _ = self.yangset.split(':')
            ctx = YSContext.get_instance(owner, self.yangset)
            ysmodels = YSYangModels(ctx, [self.yobj.model])
            for yang in ysmodels.yangs.values():
                t_walker = TreeWalker(yang.generate_tree())
                tree_walkers.append(t_walker)
            return tree_walkers

        xpaths = {}
        # Translate arg to dict if list
        if isinstance(xpaths_obj, dict):
            xpaths = {**xpaths_obj}
        elif isinstance(xpaths_obj, list):
            xpaths = dict.fromkeys(xpaths_obj, None)

        xpath_is_key = {}
        result = {}
        # Create TreeWalker instances to access get_node_by_xpath API
        tree_walkers = []
        try:
            # Cache TreeWalkers by setname and model
            if self.tree_walkers:
                if self.yangset not in self.tree_walkers:
                    tree_walkers = create_tree_walkers()
                    self.tree_walkers = {
                        **self.tree_walkers,
                        self.yangset: {
                            self.yobj.model: tree_walkers
                        }
                    }
                elif self.yobj.model not in self.tree_walkers[self.yangset]:
                    tree_walkers = create_tree_walkers()
                    self.tree_walkers[self.yangset] = {
                        **self.tree_walkers[self.yangset],
                        self.yobj.model: tree_walkers
                    }
                elif self.yobj.model in self.tree_walkers[self.yangset]:
                    tree_walkers = self.tree_walkers[self.yangset][self.yobj.model]
            else:
                tree_walkers = create_tree_walkers()
                self.tree_walkers = {
                    self.yangset: {
                        self.yobj.model: tree_walkers
                    }
                }

            for xpath, xpath_val in xpaths.items():
                if self.XP_KEY in xpath:
                    # XPath has been processed, skip it
                    result[xpath] = xpath_val
                else:
                    # Sliding window on each XPath token to determine if each slash token is key
                    tokens = [token for token in xpath.split('/') if token]
                    processed_tokens = []

                    for index in range(len(tokens)):
                        partial_xpath = '/' + '/'.join(tokens[:index + 1])
                        # This check is to prevent processing same XPath again
                        if partial_xpath not in xpath_is_key:
                            # Partial XPath has not been processed yet
                            node = None
                            for walker in tree_walkers:
                                node = walker.get_node_by_xpath(partial_xpath)
                                if node:
                                    break
                            if not node:
                                info = f'Tree walker unable to get node data for {partial_xpath}'
                                log.info(info)
                            if node and node['data']['nodetype'] == 'list':
                                xpath_is_key[partial_xpath] = True
                                processed_tokens.append(tokens[index] + self.XP_KEY)
                            else:
                                xpath_is_key[partial_xpath] = False
                                processed_tokens.append(tokens[index])

                    if processed_tokens != tokens:
                        # Key has been added to at least 1 XPath token
                        new_xpath = '/' + '/'.join(processed_tokens)
                        result[new_xpath] = xpath_val
                    else:
                        # No key detected, copy original XPath and XPath value
                        result[xpath] = xpath_val
        except Exception as e:
            log.error(e)

        # Translate results to list if arg was a list
        if isinstance(xpaths_obj, list):
            result = list(result.keys())
        return result

    @classmethod
    def label_oid_keys(cls, oids):
        """Place angle brackets for any index in any OIDs given input, given the OIDs
        are fully translated.
        Ex. .iso.org.someTable.someTableIndex.someTableData.1.2.3 ->
        .iso.org.someTable.someTableIndex.someTableData.<>

        Args:
            oids (dict/list): human readable OIDs list or dict
        Returns:
            (dict/list) - List or dict of compacted OIDs labeled by indexes (if any)
        """
        # TODO: write sanity tests
        result = None
        indexed_oids = set()
        try:
            if isinstance(oids, dict):
                result = {}
                for key, value in oids.items():
                    if cls.OID_KEY not in key:
                        oid_has_keys = False
                        # Check if there are numeric identifiers in OID
                        for token in reversed(key.split('.')):
                            if token.isdigit():
                                oid_has_keys = True
                                break
                        if oid_has_keys:
                            # Keep only alpha identifiers in OID
                            alpha_tokens = [
                                token
                                for token in key.split('.')
                                if token and not token.isdigit()
                            ]
                            alpha_tokens.append(cls.OID_KEY)
                            oid = '.' + '.'.join(alpha_tokens)
                            if oid in indexed_oids:
                                # OID has already been key-indexed, combine values of the OIDs
                                result[oid] = result[oid] + value
                            else:
                                # OID has not been key-indexed, create new mapping for OID
                                indexed_oids.add(oid)
                                result[oid] = value
                        else:
                            # This is not an key-indexed OID, return as part of result
                            result[key] = value
                    else:
                        # OID has already been key-indexed, do not process
                        result[key] = value
            elif isinstance(oids, list):
                for oid in oids:
                    if cls.OID_KEY in oid:
                        # OID already has key do not process
                        indexed_oids.add(oid)
                    else:
                        oid_has_keys = False
                        # Check if there are numeric identifiers in OID
                        for token in reversed(oid.split('.')):
                            if token.isdigit():
                                oid_has_keys = True
                                break
                        if oid_has_keys:
                            # OID has key indexes
                            # Keep only alpha identifiers in OID
                            alpha_tokens = [
                                token
                                for token in oid.split('.')
                                if token and not token.isdigit()
                            ]
                            alpha_tokens.append(cls.OID_KEY)
                            oid = '.' + '.'.join(alpha_tokens)
                            # This OID has just been indexed, add to set
                            indexed_oids.add(oid)
                        else:
                            # OID does not have key index
                            indexed_oids.add(oid)
                result = list(indexed_oids)
        except Exception as e:
            log.error(e)

        return result

    def get_oids_to_values_from_device(
        self, snmp_cmd, options=[], translate_oids=True
    ):
        """ Execute snmpwalk against a device to
            create a mapping of OIDs to corresponding
            device's values"""
        oids_to_values = {}
        # Create cmd to get OIDs to values
        cmd = []
        if self.device_password:
            # Using SNMPv3 user/password
            cmd = [
                snmp_cmd,
                '-v3',
                '-r', '5',
                '-l', 'authNoPriv',
                '-u', self.device_user,
                '-a', 'MD5',
                '-A', self.device_password
            ]
        else:
            # Community string is the user and no password
            cmd = [
                snmp_cmd,
                '-v2c',
                '-c', self.device_user,
            ]
        if translate_oids:
            cmd += [
                '-Of',
                '-Pu',
                '-M', get_path('mibs_dir'),
                '-m', 'ALL'
            ]
        # Add in device address
        cmd.append(self.address)
        # Add additional options/OIDs
        if len(options):
            cmd += options
        # Log cmd
        log.info(f'Running SNMP command: {" ".join(cmd)}')

        # Run snmp command
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, _ = process.communicate()
        if out:
            out = out.decode('utf-8', errors='replace')
            # Process stdout to create oid to values mappings
            for line in out.splitlines():
                value = ''
                line = line.strip()
                # Process each line
                tokens = line.split(': ')
                if len(tokens) == 2:
                    # TODO: convert SNMP Timeticks to Cisco UTC time
                    # and compare.
                    oid = tokens[0].split()[0]
                    value = tokens[1].strip()
                    if '(' in value and value.endswith(')'):
                        # Some OIDs had value(index) but xpath has value
                        value = value[:value.rfind('(')]
                    # Map OID to value
                    oids_to_values[oid] = value
                elif line.endswith('STRING:') or line.endswith('""'):
                    # OID has an empty str for value
                    oid = tokens[0].split()[0]
                    oids_to_values[oid] = ''

        return (oids_to_values, out)

    def _get_resp_xml(self, resp):
        """Remove XML encoding tag if it is there.

        Args:
          resp (list) or (str) or (bytes): rpc-reply returned from ncclient.
        Returns:
          str: rpc-reply in string form.
        """
        if isinstance(resp, list):
            if isinstance(resp[0], tuple):
                op, resp_xml = resp[0]
        elif isinstance(resp, (str, bytes)):
            resp_xml = str(resp)
        else:
            return ''

        if resp_xml.strip().startswith('<?xml'):
            return resp_xml[resp_xml.find('>') + 1:].strip()

        return resp_xml

    def process_rpc_reply(self, resp):
        """Transform XML into elements with associated xpath.

        Args:
          resp (list) or (str): list returned from netconf_send or
                                well formed rpc-reply XML.
        Returns:
          list: List of tuples (lxml.Element, xpath (str))
        """
        resp_xml = self._get_resp_xml(resp)

        if not resp_xml:
            log.error("No response to compare.")
            return False

        try:
            resp = ET.fromstring(resp_xml.encode('utf-8'))
        except ET.XMLSyntaxError as e:
            log.error('Response XML:\n{0}'.format(str(e)))
            log.error(traceback.format_exc())
            return False

        # if first element of reply is not 'rpc-reply' this is a bad response
        if ET.QName(resp).localname != 'rpc-reply':
            log.error("Response missing rpc-reply:\nTag: {0}".format(resp[0]))
            return False

        # Associate xpaths with response tags
        response = {}
        xpath = []
        for el in resp.iter():
            if not hasattr(el, 'text'):
                continue
            if not el.text or el.text.strip() == '':
                continue
            if ET.QName(el).localname == 'rpc-reply':
                # Don't evaluate rpc-reply tag
                continue
            if not response and ET.QName(el).localname == 'data':
                # Don't evaluate rpc-reply/data tag
                continue
            parent = el.getparent()
            xpath.append('/' + ET.QName(el).localname)
            while True:
                if parent is not None:
                    xpath.append('/' + ET.QName(parent).localname)
                    parent = parent.getparent()
                else:
                    break
            xp = ''.join(reversed(xpath)).replace('/rpc-reply/data', '')
            if xp in response:
                response[xp] += [el.text.strip()]
            else:
                response[xp] = [el.text.strip()]

            xpath = []

        return response

    def build_rpc(self, xpath=None, yang_data=None):
        if xpath is None:
            log.error('No XPath specified to build RPC with.')
            raise Exception('No XPath specified to build RPC with.')
        if yang_data is None:
            log.error('No YANG data given to build RPC with.')
            raise Exception('No YANG data given to build RPC with.')
        segments = xpath.split('/')
        seg_xp = ''
        elem = None
        nsmap = yang_data.get('root_namespace')
        curr_ns = nsmap
        curr_elem = None
        for seg in segments:
            if not seg:
                continue
            seg_xp += '/' + seg
            if elem is None:
                elem = ET.Element(
                    seg,
                    xmlns=nsmap
                )
                curr_elem = elem
                continue
            if seg_xp in yang_data:
                if yang_data[seg_xp]['namespace'] != nsmap:
                    curr_ns = yang_data[seg_xp]['namespace']
            if curr_ns != nsmap:
                ET.SubElement(
                    curr_elem,
                    seg,
                    xmlns=curr_ns
                )
                nsmap = curr_ns
            else:
                ET.SubElement(
                    curr_elem,
                    seg
                )
            curr_elem = curr_elem[0]

        filter_elem = ET.Element(
            'filter',
            xmlns='urn:ietf:params:xml:ns:netconf:base:1.0'
        )
        filter_elem.append(elem)

        return [['get', {'filter': filter_elem}]]

    def get_xpaths_to_values_from_device(self):
        """Generate dictionary of space-separated
           XPaths mapped to value in device"""
        try:
            # Send RPC through NETCONF to device
            rpc = self.build_rpc(
                self.yobj.xpaths[0].split('/')[1],
                self.yobj.yang_df
            )
            # TODO: SessionKey depends on yangsuite-netconf
            key = SessionKey(self.user, self.host)
            response = ncclient_send(key, rpc, 60)
            self.xpaths_to_values = self.process_rpc_reply(response[0][-1])
        except IndexError:
            # Response has unexpected index(es)
            log.error(
                'NETCONF response from device has unexpected index(es)'
            )
            self.xpaths_to_values = {}
        except EOFError:
            # Socket closed before all bytes could've been read
            log.error(
                'Socket closed before NETCONF response could\'ve been read'
            )
            self.xpaths_to_values = {}
        except Exception as exc:
            log.error('Unexpected Exception {0}'.format(str(exc)))
            self.xpaths_to_values = {}

        return self.xpaths_to_values

    @staticmethod
    def remove_namespace(xpaths):
        """Given a list of XPaths, remove all namespaces and return XPaths

        Returns:
            list: The list of XPaths with namespaces stripped from it
        """
        # TODO: write sanity tests
        result = []
        for xpath in xpaths:
            xp_tokens = [token for token in xpath.split('/') if token]
            xp_tokens = [token.split(':')[-1] for token in xp_tokens]
            result.append('/' + '/'.join(xp_tokens))

        return result

    def remove_keys(self, paths):
        """Given a list of XPaths or OIDs, remove keys from each element

        Args:
            paths (list): list of OIDs or XPaths in str format

        Returns:
            list: list of XPaths or OIDs with keys stripped
        """
        result = [
            path.replace(f'.{self.OID_KEY}', '')
            for path in paths
        ]
        result = [
            path.replace(self.XP_KEY, '')
            for path in result
        ]

        return result

    def run_compare(self, oid, xpath):
        """Run snmpget for OID, NETCONF get for Xpath and report returns."""
        # TODO: write updated sanity tests for this
        res_str = 'OID value "{0}" and XPath value "{1}" does not match.'
        xpaths_to_values = {}
        if not oid:
            log.error('No OID to compare.')
            raise ValueError('No OID to compare.')
        if not xpath:
            log.error('No XPath to compare.')
            raise ValueError('No XPath to compare.')
        formated_xpaths = self.remove_keys([xpath])
        formated_xpaths = self.remove_namespace(formated_xpaths)
        for xpath in formated_xpaths:
            # Build RPC using XPath to send
            rpc = self.build_rpc(xpath, self.yobj.yang_df)
            # TODO: SessionKey depends on yangsuite-netconf
            key = SessionKey(self.user, self.host)
            yang_result = ncclient_send(key, rpc, 60)
            val_xpath = self.process_rpc_reply(yang_result[0][1])
            xpaths_to_values[xpath] = val_xpath.get(xpath, 'No data returned from XPath.')
            # Get OID result
            try:
                # If there is a key, remove key and getnext from removed key OID
                # Use snmpwalk regardless, sometimes value being mapped is a table
                oid_result, oid_str = self.get_oids_to_values_from_device(
                    'snmpwalk',
                    options=self.remove_keys([oid])
                )
            except Exception as exc:
                return {'result': str(exc)}
            if not oid_result:
                res_str = res_str.format(str(None), val_xpath)
                return {'result': res_str}
            if xpath not in val_xpath:
                val_xpath[xpath] = 'No data returned from XPath.'
        # Format result into string to be displayed in dialog
        result_str = f'SNMPGET:\n{oid_str}\n\n'
        for xpath in xpaths_to_values:
            result_str += f'YANG GET:\n{xpath}\nVALUES:\n{xpaths_to_values[xpath]}'
        return {'result': result_str}
