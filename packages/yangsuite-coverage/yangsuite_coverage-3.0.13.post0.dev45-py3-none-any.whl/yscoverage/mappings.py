#! /usr/bin/env python
# Copyright 2021 Cisco Systems Inc, All rights reserved.
import os
import io
import uuid
import pandas as pd
from functools import reduce
from concurrent import futures

from yangsuite import get_logger

log = get_logger(__name__)


def merge_dictionaries(a, b, path=None):
    """Merge dictionary b into dictionary a"""
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dictionaries(a[key], b[key], path + [str(key)])
            elif a[key] == b[key] or isinstance(a[key], type(b[key])):
                # same leaf value
                pass
            else:
                raise Exception('Conflict at %s' % '.'.join(
                    path + [str(key)]
                ))
        else:
            a[key] = b[key]
    return a


def get_tree_dict(oid):
    """Get a nested dict using the OID indexes as keys

    Args:
        oid (str): OID in str format
    """
    dot_tokens = [
        token for token in oid.split('.') if token]
    tree_dict = reduce(
        lambda res, cur: {cur: res},
        reversed(dot_tokens),
        {}
    )

    return tree_dict


class MappingException(Exception):
    pass


class MibYangWriter:

    writers = {}

    def __init__(
        self, map_file, user, mib_paths=[], yang_paths=[], mod_xp={}, mod=''
    ):
        self.user = user
        self.module_matches = mod_xp
        self.module = mod
        self.map_file = map_file
        self.mib_paths = mib_paths
        self.yang_paths = yang_paths

    @classmethod
    def get(
        cls, map_file, user, mib_paths=[], yang_paths=[], mod_xp='', mod=''
    ):
        writer = cls.writers.get((map_file, user))
        if not writer:
            writer = cls(map_file, user, mib_paths, yang_paths, mod_xp, mod)
            cls.writers[(map_file, user)] = writer
        return writer

    @classmethod
    def delete(cls, map_file, user):
        if (map_file, user) in cls.writers:
            del cls.writers[(map_file, user)]

    @classmethod
    def get_mapping_data(cls, file_ref, translate_oids):
        mib_paths = []
        mib_path_to_yang_path = {}
        modules_to_matched_xpaths = {}
        yang_paths = []
        path = ''
        tree = {}

        if isinstance(file_ref, io.StringIO):
            path = file_ref
        elif os.path.isfile(file_ref):
            path = file_ref

        if path:
            mapped_df = cls.read_map_file(path)
            for dfrow in mapped_df.iterrows():
                row = dfrow[1].to_dict()
                oid = row.get('OID')
                numeric_oid = row.get('Numeric OID', translate_oids([oid], to_numeric=True)[-1])
                xpath = row.get('YANG Xpath')
                model = row.get('YANG Module')
                if xpath:
                    xpath_obj = {
                        'label': xpath,
                        'value': xpath,
                        'model': model,
                        'id': uuid.uuid4().__str__()
                    }
                    mib_path_to_yang_path[oid] = xpath_obj
                    modules_to_matched_xpaths[xpath] = model
                    yang_paths.append(xpath_obj)
                mib_paths.append({
                    'oid': oid,
                    'numeric': numeric_oid,
                    'value': oid,
                    'id': uuid.uuid4().__str__()
                })
                # Do not render N/A OIDs
                if 'n/a' not in oid.lower():
                    curr_tree = get_tree_dict(oid)
                    if tree:
                        # Merge this tree to the main tree
                        tree = merge_dictionaries(tree, curr_tree)
                    else:
                        # No tree exists yet, create it
                        tree = curr_tree

        return (
            mib_paths,
            yang_paths,
            mib_path_to_yang_path,
            modules_to_matched_xpaths,
            tree
        )

    @classmethod
    def read_map_file(self, filepath):
        try:
            if os.path.isfile(filepath):
                # open and read
                mapped_df = pd.read_csv(
                    filepath,
                    keep_default_na=False,
                    index_col=False,
                )
                return mapped_df
        except Exception:
            if os.path.isfile(filepath):
                # open and read
                mapped_df = pd.read_excel(
                    filepath,
                    sheet_name='Mapped',
                    keep_default_na=False,
                    engine='openpyxl',
                )
                return mapped_df
        return None

    def _write_xlsx(self, mapped_df):
        """Not writing xlsx files right now."""
        writer = pd.ExcelWriter(self.map_file, engine='xlsxwriter')
        mapped_df.to_excel(writer, sheet_name='Mapped', index=False)

        bold = writer.book.add_format({'bold': True})
        s1 = writer.sheets['Mapped']
        s1.set_column(0, 1, 75)
        s1.set_row(0, None, bold)

        writer.save()

    def _write_csv(self, mapped_df):
        mapped_df.to_csv(
            self.map_file,
            index=False
        )
        if not os.path.isfile(self.map_file):
            raise MappingException('Save mapping file failed.')

    def save_mapping_in_csv(
        self, oid=None, mib_to_yang_paths={},
        mibyang_path=None
    ):
        """Save a mapping in the local mapping file repository

        Args:
            oid (str): User selected OID
            ypaths (list): YANG XPaths
            mib_to_yang_paths (dict): OIDs mapped to YANG XPaths
        """
        try:
            if mibyang_path:
                if mibyang_path.yobj.model != self.module:
                    # This happens when user match OIDs to XPaths using a diff. model
                    self.module = mibyang_path.yobj.model
        except Exception:
            pass
        if os.path.isfile(self.map_file):
            # open and read
            mapped_df = self.read_map_file(self.map_file)
            for mapped_oid, xpath in mib_to_yang_paths.items():
                if xpath and mapped_oid == oid:
                    # Invalid types for MIB to YANG mappings
                    if isinstance(xpath, list):
                        xpath = xpath[-1].get('value', '')
                    elif isinstance(xpath, dict):
                        xpath = xpath.get('value', '')
                    # Label XPath with key(s)
                    xpath = mibyang_path.label_xpath_keys([xpath])[-1]

                    if mapped_df.loc[mapped_df['OID'] == oid].empty:
                        # This is new walk with existing map file
                        mapped_df.loc[len(mapped_df.index)] = [
                            oid,
                            mibyang_path.translate_oids([oid], to_numeric=True)[-1],
                            xpath,
                            self.module
                        ]
                    elif mapped_df.loc[
                        mapped_df['OID'] == oid, 'YANG Xpath'
                    ].values[0] == xpath:
                        # Unchanged mapping
                        continue
                    else:
                        # New mapping
                        mapped_df.loc[
                            mapped_df['OID'] == oid, 'YANG Xpath'
                        ] = xpath
                        mapped_df.loc[
                            mapped_df['OID'] == oid, 'Numeric OID'
                        ] = mibyang_path.translate_oids([oid], to_numeric=True)[-1]
                        mapped_df.loc[
                            mapped_df['OID'] == oid, 'YANG Module'
                        ] = self.module
        else:
            mapped_dict = {
                'OID': [],
                'Numeric OID': [],
                'YANG Xpath': [],
                'YANG Module': []
            }
            for mib_path in self.mib_paths:
                oid = mib_path['oid']
                numeric_oid = mib_path.get(
                    'numeric',
                    mibyang_path.translate_oids([oid], to_numeric=True)[-1]
                )
                if oid in mib_to_yang_paths and mib_to_yang_paths[oid]:
                    # Parse XPath obj and label keys
                    xpath_obj = mib_to_yang_paths[oid]
                    if isinstance(xpath_obj, dict):
                        xpath = xpath_obj.get('value', '')
                    else:
                        xpath = xpath_obj
                    if mibyang_path:
                        # Label XPath with key(s)
                        xpath = mibyang_path.label_xpath_keys([xpath])[-1]

                    mapped_dict['OID'].append(oid)
                    mapped_dict['Numeric OID'].append(numeric_oid)
                    mapped_dict['YANG Xpath'].append(xpath)
                    mapped_dict['YANG Module'].append(self.module)

            mapped_df = pd.DataFrame(mapped_dict)
        self._write_csv(mapped_df)

    def delete_mapping_in_csv(self, oid):
        """Delete a single mapping by removing YANG XPath from target row

        Args:
            oid (str): Identifier in MIB hierarchy
            mib_file (str): MIB module name
            yang_module (str): YANG module name
        """
        if os.path.exists(self.map_file):
            mapped_df = self.read_map_file(self.map_file)
            # Find xpath at OID row
            ypath = mapped_df.loc[mapped_df.OID == oid]
            if len(ypath) == 0:
                raise KeyError('OID "{0}" not found'.format(oid))
            # Delete all rows in CSV that has OID
            mapped_df = mapped_df[mapped_df['OID'] != oid]

            self._write_csv(mapped_df)

    @classmethod
    def find_mappings(cls, oids, filepath, filename, translate_oids, label_oid_keys):
        def process_rows(df_rows, translate_oids, label_oid_keys):
            """Process rows in Dataframe to add filename and numeric
            OID translation (if needed)

            Args:
                df_row (list): list format of row in Dataframe

            Raises:
                ValueError: error is raised when invalid number of
                row elems is encountered (not 3 or 4)

            Returns:
                list: list of 5 elements representing 1 row of mapping
            """
            rows = []
            for df_row in df_rows:
                if len(df_row) not in [3, 4]:
                    # Wrong CSV format
                    err = f'Invalid number of columns in CSV: {len(df_row)} columns found.'
                    log.error(err)
                    raise ValueError(err)
                elif len(df_row) == 3:
                    readable_oid = label_oid_keys(translate_oids([df_row[0]]))[-1]
                    numeric_oid = translate_oids([readable_oid], to_numeric=True)[-1]
                    row = [
                        # Readable OID
                        readable_oid,
                        # Translated numeric OID element
                        numeric_oid,
                        # XPath, and YANG module
                        *df_row[1:],
                        filename
                    ]
                elif len(df_row) == 4:
                    # New version of CSV
                    row = [
                        *df_row,
                        filename
                    ]
                rows.append(row)

            return rows

        MAX_WORKERS = 4
        rows = []
        columns = []
        mapped_df = cls.read_map_file(filepath)

        if not mapped_df.empty:
            # Get column names for frontend to display
            columns = mapped_df.columns.tolist()
            if len(columns) == 3:
                columns = [
                    columns[0],
                    # Add Numeric OIDs column to this old version CSV
                    'Numeric OID',
                    *columns[1:]
                ]
            # Always add in filename column
            columns.append('File Name')
            # Populate rows to display in frontend table
            for oid in oids:
                contains_oid = mapped_df['OID'].str.contains(oid)
                filtered_df = mapped_df[contains_oid]
                df_rows = filtered_df.values.tolist()
                df_rows_parts = [
                    df_rows[i: i + MAX_WORKERS]
                    for i in range(0, len(df_rows), MAX_WORKERS)
                ]
                with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    # Rows with length 3 does not have numeric OIDs, add translation
                    future_objs = [
                        executor.submit(
                            process_rows,
                            part,
                            translate_oids,
                            label_oid_keys
                        )
                        for part in df_rows_parts
                    ]
                    done, _ = futures.wait(future_objs)
                    if len(done) == len(future_objs):
                        for future in future_objs:
                            if future.exception() is not None:
                                log.error(future.exception())
                                raise ValueError(future.exception())
                            else:
                                rows.extend(future.result())
        return (rows, columns)


def process_import_data(file_data, file_path, user):
    """Extract MIB/YANG paths and mappings from frontend data

    Args:
        file_data (list): List of mapped and unmapped dict.

    Returns:
        tuple: OIDs list, YANG XPaths list, and MIB to YANG path map
    """
    yang_paths = []
    mib_paths = []
    mib_to_yang_paths = {}

    for data in file_data:
        if 'mapped' in data and isinstance(data['mapped'], str):
            # string buffer
            with open(file_path, 'w') as fd:
                fd.write(data['mapped'])
            break
        elif isinstance(data, dict):
            mapped = data['mapped']
            for mapping in mapped:
                if len(mapping) >= 2:
                    oid = mapping[0]
                    ypath = mapping[1]
                elif len(mapping) == 1:
                    oid = mapping[0]
                    ypath = None
                else:
                    log.error('Invalid mapping {0}'.format(str(mapping)))
                    continue
                if oid == 'OID':
                    # header row
                    continue
                if ypath:
                    mib_to_yang_paths[oid] = ypath
                mib_paths.append({
                    'oid': oid,
                    'value': oid,
                    # Random ID to help frontend rendering
                    'id': uuid.uuid4().__str__()
                })

        myw = MibYangWriter.get(
            file_path,
            user,
            mib_paths,
            yang_paths
        )
        myw.save_mapping_in_csv(mib_to_yang_paths=mib_to_yang_paths)

    return (mib_paths, yang_paths, mib_to_yang_paths)


def show_mapping_data(filepath, user, translate_oids):
    if not os.path.isfile(filepath):
        raise MappingException('Cannot locate {0}'.format(filepath))
    myw = MibYangWriter(filepath, user)
    return myw.get_mapping_data(myw.map_file, translate_oids)
