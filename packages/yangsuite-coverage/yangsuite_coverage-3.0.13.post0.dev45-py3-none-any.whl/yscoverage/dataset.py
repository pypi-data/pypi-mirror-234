# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
# ! /usr/bin/env python
"""Script to detect YANG model changes between 2 repositories."""
import os
import tempfile
from zipfile import ZipFile
import pandas
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ysyangtree.yangsettree import get_trees
from ysfilemanager import YSYangSet, YSYangDirectoryRepository, merge_user_set
from ysyangtree import YSContext, YSYangModels
from ysyangtree.ymodels import ALL_NODETYPES, DEFAULT_INCLUDED_NODETYPES
from yangsuite import get_logger

log = get_logger(__name__)


ALL_COLUMNS = [
    "xpath",
    "nodetype",
    "module",
    "datatype",
    "basetype",
    "leafref_path",
    "when",
    "must",
    "deviation",
    "mandatory",
    "patterns",
    "name",
    "description",
    "revision",
    "xpath_pfx",
    "base",
    "prefix",
    "namespace",
    "schema_node_id",
    "access",
    "operations",
    "key",
    "presence",
    "default",
    "options",
    "min",
    "max",
    "typespec",
    "units",
    "members",
    "fraction_digits",
    "minLength",
    "maxLength",
]


class YSYangDatasetException(Exception):
    """Pre-commit exception."""
    pass


def dataset_for_yangset(owner, setname, model, addons=None,
                        reference=None, all_data=False):
    try:
        ys = YSYangSet.load(owner, setname)
    except (OSError, ValueError):
        raise YSYangDatasetException('No such yangset "{0}"'
                                     .format(merge_user_set(owner, setname)))
    except RuntimeError:
        raise YSYangDatasetException('No such user "{0}"'.format(owner))
    return _dataset_for_repo(ys, model, addons,
                             reference=reference,
                             yangset=merge_user_set(owner, setname),
                             all_data=all_data)


def dataset_for_directory(path, model, addons=None, reference=None,
                          all_data=False):
    try:
        repo = YSYangDirectoryRepository(path)
    except OSError:
        raise YSYangDatasetException('Invalid path "{0}"'.format(path))
    return _dataset_for_repo(repo, model, addons, reference=reference,
                             all_data=all_data)


def _dataset_for_repo(repo, model, addons=None, reference=None,
                      yangset=None, all_data=False):
    """Logic shared between dataset_for_yangset and dataset_for_directory."""
    models = YSYangModels.get_instance(reference)
    if ((not models) or
            model not in models.modelnames or
            models.ctx.repository != repo or
            models.ctx.repository.is_stale):
        ctx = YSContext.get_instance(reference, yangset)
        if not ctx:
            ctx = YSContext(repo, reference, [model])
        models = YSYangModels(ctx, [model])
        # We are intentionally not storing it due to memory/performance
        # issue

    if not addons:
        addons_list = []
    else:
        addons_list = list(addons)

    # Add module to addons list
    if 'module' not in addons_list:
        addons_list.insert(0, 'module')

    addons = addons_list

    data = []
    if models.yangs[model]:
        if 'data' in models.yangs[model].tree:
            if 'modtype' in models.yangs[model].tree['data']:
                modtype = models.yangs[model].tree['data']['modtype']
                if modtype == 'submodule':
                    log.warning("%s is a submodule.", model)
                    models = YSYangModels(ctx, [model],
                                          included_nodetypes=ALL_NODETYPES)
                    for m, parser in models.yangs.items():
                        if m == model:
                            data = parser.tw.get_dataset_using_key(
                                parser.tw.tree,
                                'name',
                                [],
                                '',
                                *addons
                            )

        for m, parser in models.yangs.items():
            data += parser.tw.get_dataset(parser.tw.tree, [], *addons)

    if not all_data:
        # Trim down dataset
        to_dataset = []
        for to_data in data:
            if model in to_data:
                to_dataset.append(to_data)
        data = to_dataset

    return {'header': ['xpath'] + list(addons),
            'data': data}


class YSDataSet:
    """Dataset for a yangset or directory in Pandas DataFrame format."""
    def __init__(self, owner=None, setname=None, yang_dir=None):
        self.owner = owner
        self.setname = setname
        self.yang_dir = yang_dir
        self.dfs = {}
        self.df_diffs = {}
        self.csv_file = ''
        self.channel_layer = get_channel_layer()

    """Send async status updates to the websocket client.

    Args:
      message (str): Message to send to client.
    """
    def send_websocket_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            str(hash(str(self.owner) + 'datasetinfo')),
            {
                'type': 'dataset_state_update',
                'message': {'progress': message}
            }
        )

    def get_tree_from_directory(
            self, modules, nodes=DEFAULT_INCLUDED_NODETYPES
            ):
        """Get a jstree from a directory of yang files.

        Args:
            modules (list): List of modules to include in the tree.
            nodes (list): List of node types to include in the tree.
        Return:
            (dict): jstree dictionary.
        """
        tree = []
        if self.yang_dir is not None:
            repo = YSYangDirectoryRepository(self.yang_dir)
            ctx = YSContext(repo, self.owner, modules)
            tree = YSYangModels(
                ctx, modules, included_nodetypes=nodes
            )
            return tree.jstree['data']
        log.error('No yang directory specified')
        return tree

    def get_dataset_trees(self, modules, nodes=DEFAULT_INCLUDED_NODETYPES):
        """Get a jstree from a yangset.

        Args:
            modules (list): List of modules to include in the tree.
            nodes (list): List of node types to include in the tree.
        Return:
            (dict): jstree dictionary.
        """
        trees = []
        if self.yang_dir:
            trees = self.get_tree_from_directory(modules)
        else:
            trees = get_trees(
                self.owner,
                self.setname,
                modules,
                nodes=nodes
            )
        return trees

    def get_pandas_df(self, node, df_list=[], group=''):
        """Get dict for creation of pandas DataFrame (recursive).

        Args:
            node (dict): jstree dictionary.
            df_list (list): List of dictionaries to populate.
            group (str): "grouping" nodetype will be the parent for non-xpath.
                         nodes.
                         "container" and "list" nodetypes will contribute to
                         the xpath.
        Return:
            (list): List of dictionaries.
        """
        if node and 'data' in node and 'modtype' not in node['data']:
            if 'xpath' not in node['data']:
                if group:
                    node['data']['xpath'] = '/' + group
                    if node['data']['name'] != group:
                        node['data']['xpath'] += '/' + node['data']['name']
                    if node['data']['nodetype'] in [
                        'container', 'list', 'choice', 'case'
                    ]:
                        group += '/' + node['data']['name']
                else:
                    node['data']['xpath'] = '/' + node['data']['name']
            df_list.append(node['data'])
        if 'children' in node:
            for child in node['children']:
                if child['data']['nodetype'] == 'grouping':
                    group = child['data']['name']
                self.get_pandas_df(child, df_list, group)
        return df_list

    def dataset_for_pandas(
            self, modules, columns=ALL_COLUMNS,
            format='json', add_support=True
            ):
        """Get a pandas DataFrame from a jstree.

        Args:
            modules (list): List of modules to include in the tree.
            columns (list): List of columns to include in the DataFrame.
            format (str): json or csv.
            add_support (bool): Add support modules to dataset.
        Return:
            (pandas.DataFrame): DataFrame appended to class list "dfs".
        """
        dt_now = datetime.now()
        self.send_websocket_message(
            f'Get trees...this may take some time...start: {dt_now.strftime("%H:%M:%S")}'  # noqa
        )
        # Always try to get DEFAULT_INCLUDED_NODETYPES first.
        trees = self.get_dataset_trees(modules)

        self.send_websocket_message('Creating datasets...')

        for tree in trees:
            if 'text' not in tree:
                log.error(f'NO TREE IN DATA:\n{tree}')
                continue
            if 'children' in tree:
                self.send_websocket_message(
                    f'{tree["text"]} tree dataset...'
                )
                log.debug(
                    f"{tree['text']} {dt_now.strftime('%H:%M:%S')}."
                )
                if tree['text'] in self.dfs:
                    continue
                df_list = self.get_pandas_df(tree, [])
                if len(df_list):
                    df = pandas.DataFrame(df_list, columns=columns)
                    if format == 'json':
                        # Clean up nan for web page display
                        df.fillna('', inplace=True)
                    self.dfs[tree['text']] = df
            elif add_support:
                # No children so try ALL_NODETYPES
                self.send_websocket_message(
                    f'{tree["text"]} support tree dataset...'
                )
                support_tree = self.get_dataset_trees(
                    [tree['text']], ALL_NODETYPES
                )
                tree = support_tree[0]
                if 'text' not in tree:
                    log.error(f'NO TREE IN DATA:\n{tree}')
                    continue
                log.debug(
                    f"{tree['text']} {dt_now.strftime('%H:%M:%S')} support."
                )
                if 'children' not in tree:
                    log.info(f'NO CHILDREN IN DATA:\n{tree["text"]}')
                    if 'data' in tree:
                        tree['data']['name'] = tree['text']
                        tree['data']['description'] = tree.get(
                            'description', ''
                        )
                    else:
                        log.error(f'NO DATA: {tree["text"]}')
                        continue
                df_list = self.get_pandas_df(tree, [])
                if len(df_list):
                    df = pandas.DataFrame(df_list, columns=columns)
                    self.dfs[tree['text']] = df
        self.send_websocket_message('Datasets done')
        if format == 'csv':
            if not self.dfs:
                return
            tmpdir = tempfile.gettempdir()
            if os.path.isfile(os.path.join(tmpdir, 'dataset.zip')):
                os.remove(os.path.join(tmpdir, 'dataset.zip'))

            for mod in self.dfs.keys():
                self.dfs[mod].to_csv(os.path.join(tmpdir, mod + '.csv'))
                with ZipFile(os.path.join(tmpdir, 'dataset.zip'), 'a') as zf:
                    zf.write(
                        os.path.join(tmpdir, mod + '.csv'),
                        arcname=os.path.join('dataset', mod + '.csv')
                    )
            self.csv_file = os.path.join(tmpdir, 'dataset.zip')

    def _apply_match(self, row, df):
        if row['xpath'] not in df['xpath'].values:
            # this xpath does not reside in model
            row['match'] = False
        else:
            row['match'] = True
        return row

    def dataset_model_diff(self, compare_ds, format='json'):
        """Compare dataset to class dataset and return differences.

        Args:
            compare_ds (YSDataSet): Dataset to compare.
            format (str): json or csv.
        """
        if not self.dfs or not compare_ds.dfs:
            return

        for module in self.dfs.keys():
            if module in compare_ds.dfs:
                base_df = self.dfs[module]
                comp_df = compare_ds.dfs[module]
                base_name = self.setname or os.path.basename(self.yang_dir)
                comp_name = compare_ds.setname or os.path.basename(
                    compare_ds.yang_dir
                )
                self.send_websocket_message(f'{module}...match xpaths')
                # match base_df xpaths with comp_df xpaths
                match_base_df = base_df.apply(
                    self._apply_match,
                    axis=1,
                    **{'df': comp_df}
                )
                self.send_websocket_message(f'{module}...find base removed')
                # xpaths in base_df that don't match have been removed
                rm_df = match_base_df[match_base_df['match'] == False]  # noqa
                if not rm_df.empty:
                    rm_df.drop('match', axis=1, inplace=True)
                match_base = match_base_df[match_base_df['match'] == True]  # noqa

                # len(match_base) == len(base_df) means they match everything
                # match comp_df xpaths with base_df xpaths
                match_comp_df = comp_df.apply(
                    self._apply_match,
                    axis=1,
                    **{'df': base_df}
                )
                self.send_websocket_message(f'{module}...find compare new')
                # xpaths in comp_df that don't match in base_df are new
                new_df = match_comp_df[match_comp_df['match'] == False]  # noqa

                # filter out new rows from comp_df for compare
                match_comp = None
                if not new_df.empty:
                    new_df.drop('match', axis=1, inplace=True)
                match_comp = match_comp_df[match_comp_df['match'] == True]  # noqa

                # have recoded new xpaths and removed xpaths, now compare
                comp_drp = match_comp.drop('match', axis=1)
                base_drp = match_base.drop('match', axis=1)

                # Sort order of rows by xpath.
                comp_sort = comp_drp.sort_values('xpath')
                comp_idx = comp_sort.reset_index(drop=True)
                base_sort = base_drp.sort_values('xpath')
                base_idx = base_sort.reset_index(drop=True)
                self.send_websocket_message(f'{module}...find changes')
                # compare match rows to base rows and return diff
                try:
                    df_diff = base_idx.compare(
                        comp_idx,
                        keep_shape=True,
                        align_axis=0,
                        result_names=(
                            comp_name, base_name)
                    )
                except TypeError:
                    # Need pandas 1.5.3 or later for "result_names" parameter.
                    log.error("Update pandas to 1.5.3 or later.")
                    df_diff = base_idx.compare(
                        comp_idx,
                        keep_shape=True,
                        align_axis=0
                    )
                df_diff.dropna(how='all', inplace=True)
                df_diff.dropna(axis=1, how='all', inplace=True)

                xpaths = []
                for idx in df_diff.index:
                    xpaths.append(comp_idx.iloc[idx[0]].xpath)
                df_diff.insert(0, 'xpath', xpaths)

                df_diff.fillna('', inplace=True)
                self.df_diffs[module] = {
                    'diff': df_diff,
                    'new': new_df,
                    'removed': rm_df
                }

        if not self.df_diffs:
            self.send_websocket_message('No differences found')
            self.send_websocket_message('done')
            return

        if format == 'csv':
            tmpdir = tempfile.gettempdir()
            if os.path.isfile(os.path.join(tmpdir, 'diffset.zip')):
                os.remove(os.path.join(tmpdir, 'diffset.zip'))

            for mod, data in self.df_diffs.items():
                diff_file = new_file = rm_file = None
                if not data['diff'].empty:
                    diff_file = os.path.join(tmpdir, mod + '.diff.csv')
                    data['diff'].to_csv(diff_file)
                if not data['new'].empty:
                    new_file = os.path.join(tmpdir, mod + '.new.csv')
                    data['new'].to_csv(new_file)
                if not data['removed'].empty:
                    rm_file = os.path.join(tmpdir, mod + '.removed.csv')
                    data['removed'].to_csv(rm_file)
                with ZipFile(os.path.join(tmpdir, 'diffset.zip'), 'a') as zf:
                    if diff_file:
                        zf.write(
                            diff_file,
                            arcname=os.path.join('diffset', mod + '.diff.csv')
                        )
                    if new_file:
                        zf.write(
                            new_file,
                            arcname=os.path.join('diffset', mod + '.new.csv')
                        )
                    if rm_file:
                        zf.write(
                            rm_file,
                            arcname=os.path.join(
                                'diffset', mod + '.removed.csv'
                            )
                        )
            self.csv_file = os.path.join(tmpdir, 'diffset.zip')
            self.send_websocket_message('done')


def get_modules(yang_dir=None, owner=None, setname=None, category=None):
    """Get a list of modules from a directory or yangset.

    Args:
        yang_dir (str): Directory containing yang files.
        owner (str): User name.
        setname (str): Yangset name.
        category (str): Category name (must be in name of module).
    Return:
        (list): List of modules.
    """
    modules = []

    if yang_dir and not os.path.isdir(yang_dir):
        raise YSYangDatasetException(f'Directory not found: {str(yang_dir)}')

    if category and yang_dir:
        for f in os.listdir(yang_dir):
            if f.endswith('.yang') and category in f:
                f = f.replace('.yang', '')
                modules.append(f[:f.find('@')])
    elif category and owner and setname:
        try:
            ys = YSYangSet.load(owner, setname)
            if not os.path.isdir(ys.repository.path):
                raise YSYangDatasetException(
                    f'Repository not found: {ys.repository.path}'
                )
            for mod, _, _ in ys.get_modules_and_revisions():
                if 'deviation' in mod:
                    # Not parsed because the changes are already in jstree.
                    continue
                if category in mod:
                    modules.append(mod)
        except FileNotFoundError:
            raise YSYangDatasetException(f'Yangset not found: {setname}')
    else:
        raise YSYangDatasetException('Require directory, or yangset')

    return modules


def get_module_dataset(format, yang_dir=None, owner=None, base_set=None,
                       columns=[], modules=[], compare_set=None,
                       category=None, add_support=False):
    """Populate/compare YSDataSet classes from a directory or yangset.

    Args:
        format (str): json or csv.
        yang_dir (str): Directory containing yang files.
        owner (str): User name.
        base_set (str): Yangset name.
        columns (list): List of columns to include in the DataFrame.
        modules (list): List of modules to include in the tree.
        compare_set (str): Yangset name to compare.
        category (str): Category name (must be in name of module).
        add_support (bool): Add support modules to dataset.
    Return:
        (YSDataSet): Dataset.
    """
    base_ds = YSDataSet(owner, base_set, yang_dir)
    if not modules:
        if not category:
            raise YSYangDatasetException('No category and no modules')
        modules = get_modules(yang_dir, owner, base_set, category)
    base_ds.dataset_for_pandas(modules, columns, format, add_support)

    if compare_set:
        compare_ds = YSDataSet(owner, compare_set, yang_dir)
        compare_ds.dataset_for_pandas(modules, columns, format, add_support)
        base_ds.dataset_model_diff(compare_ds, format)

    return base_ds
