"""Report Model Coverage"""
import os
import argparse
import glob
import subprocess
import shutil
import re
import tempfile
import json
import logging
import lxml.etree as et
import zipfile
import yaml
import pandas as pd
from yscoverage.dataset import dataset_for_directory
from yscoverage.yangdiff import getdiff
from ysyangtree.tasks import TaskHandler
from yangsuite.logs import get_logger

# Suppress verbose logging messages from being echoed to console when
# running as CLI script
get_logger('yangsuite.ysyangtree.context').setLevel(logging.ERROR)
get_logger('yangsuite.ysyangtree.ymodels').setLevel(logging.ERROR)
logger = get_logger('model-coverage')

# Template pattern
var_pattern = re.compile(r"{{.*}}|_-.*-_")
var_template = ['{{', '_-']

# Do not write log to console by default
console_log = False
# Dictionary for all test cases
all_tc_dict = dict()

# Model Paths
MODELPATH = '/mgmt/dmi/model/yang/src/'
TDLMODELPATH = '/mgmt/dmi/libyang/'
MODELDIRS = [MODELPATH + 'ned/',
             MODELPATH + 'openconfig/',
             TDLMODELPATH]


def setup_args():
    """Setup and return command line parameter parser object. """
    parse = argparse.ArgumentParser(description='DMI Precommit Check Tool',
                                    epilog="""
    Example:
    Precommit Check Tool:
    python precommit-check.py -ws path_to_workspace -dir working_dir
                              -label branch
    """)

    parse.add_argument('-ws', '--workspace', type=str, dest='workspace',
                       required=False,
                       help='Path to the workspace to run precommit against')

    parse.add_argument('-label', '--label', type=str, dest='label',
                       required=False,
                       help='Branch name')

    parse.add_argument('-reportname', '--reportname', type=str,
                       dest='reportname',
                       required=False,
                       help='Model name')

    parse.add_argument('-bugid', '--bugid', type=str, dest='bugid',
                       required=False,
                       help='Bugid')

    parse.add_argument('--report', action='store_true',
                       required=False,
                       help='Generate model coverage report')

    parse.add_argument('-logfile', '--logfile', type=str, dest='logfile',
                       required=False,
                       help='Log file')
    parse.add_argument('-modelpath', '--modelpath', type=str, dest='modelpath',
                       required=False,
                       help='Model Path')
    return parse


def report_result(msg, fd):
    """Write results to console and/or file."""
    if console_log:
        print(msg)
    fd.write(msg + '\n')


def print_invalid_testcases(testcases, header, f):
    """Print invalid test cases.

    Args:
        testcases (dict): A dictionary of test xpaths and its
                          corresponding test files
        header (str): report header
        f (int): file descriptor
    """
    print_header = False

    for k, v in testcases.items():
        if not print_header:
            report_result('  ' + header, f)
            report_result('  ' + len(header)*'=', f)
            print_header = True
        report_result('  ' + k, f)
        report_result('   ' + v, f)

    if testcases:
        report_result('\n', f)


def run_cmd(cmd, wdir=None):
    """Execute a command line.

    Args:
        cmd (str): the command to be executed
        wdir (str): path to the workspace

    Return:
        (str): output of the command
    """
    if not wdir:
        wdir = os.getcwd()
    logger.debug("Calling: %s", ''.join(cmd))
    return subprocess.check_output(cmd,
                                   cwd=wdir,
                                   stderr=subprocess.STDOUT).decode()


def get_git_changeset(logfile, wspath):
    """Retrive a list of modified model files from a git ws.

    Args:
        logfile (str): absolute path to the file to write output to
        wspath (str): path to the workspace

    Return:
        ret (int): return status
    """
    ret = 0
    command = ['git', 'diff', '--name-only', '--diff-filter=AM']
    with open(logfile, 'w') as f:
        ret = subprocess.call(command,
                              cwd=wspath,
                              stdout=f,
                              stderr=subprocess.PIPE)

    return ret


def copy_tdl_base_model(tdlpath, workspace, base_workspace):
    """Copy tdl models to the baseline git ws.

    Args:
        tdlpath (str): path to the tdl transform file
        workspace (str): path to the workspace
        base_workspace (str): path to the baseline workspace

    Return:
        ret (int): return status
    """
    # tdlpath: 'binos/mgmt/dmi/libyang/src/yang/Cisco-IOS-XE-bgp-oper.yang'
    modelpath = os.path.splitext(tdlpath)[0]
    # modelpath: 'binos/mgmt/dmi/libyang/src/yang/Cisco-IOS-XE-bgp-oper'
    mn = os.path.basename(modelpath)

    src_path = os.path.join('binos/mgmt/dmi/model/tests/tdl-oper',
                            mn,
                            'baseline')
    dst_path = os.path.join(strip_tdlmodelpath(), 'model')

    full_src_path = os.path.join(workspace, src_path, mn + '.yang')
    full_dst_path = os.path.join(base_workspace, dst_path)

    shutil.copy(full_src_path, full_dst_path)
    return


def copy_base_model(model_path, workspace, label, base_workspace):
    """Copy baseline models to the baseline git ws.

    Args:
        model_path (str): path to the model from binos directory
        workspace (str): path to the workspace
        base_workspace (str): path to the baseline workspace

    Return:
        ret (int): return status
    """
    ret = 0
    # copy model from origin/<label>
    origin_str = 'origin/' + label + ':' + model_path
    command = ['git', 'show', origin_str]

    sha = ''
    output = run_cmd(['git', 'branch', '-vv'], workspace)

    # output of 'git branch -vv'
    # * (HEAD detached at V1612_1SPRD3_FC1) dc999411eeeb CSCvr02304 Boot ...
    # s2c/polaris_dev                       8f31b9cf1285 [origin/s2c/polar ...
    if output.startswith('*'):
        # commit sha is in the third column
        sha = output.split(' ')[2]

        if sha:
            # copy model from sha
            origin_str = sha + ':' + model_path
            # git show dc999411eeeb:./Cisco-IOS-XE-wccp.yang
            command = ['git', 'show', origin_str]

    tmp_line = os.path.relpath(model_path, 'binos')
    with open(os.path.join(base_workspace, tmp_line), 'w') as f:
        ret = subprocess.call(command,
                              cwd=workspace,
                              stdout=f,
                              stderr=subprocess.PIPE)

    return ret


def get_acme_changeset(logfile, wspath):
    """Retrive a list of modified model files from an acme ws.

    Args:
        logfile (str): the command to be executed
        wspath (str): path to the workspace

    Return:
        None
    """
    command = ['acme', 'lschangeset']
    with open(logfile, 'w') as f:
        # ignore return code
        subprocess.call(command,
                        cwd=wspath,
                        stdout=f,
                        stderr=subprocess.PIPE)

    with open(logfile, 'r') as f:
        for line in f.readlines():
            if line.startswith('Component: '):
                chgsetver = line.split('Component: ')[-1]
                return chgsetver

    return None


def pull_baseline_acme_ws(projlu_fullpath, comp_ver,
                          label, base_workspace):
    """Pull a baseline acme ws.

    Args:
        projlu_fullpath (str): path to .projlu for dmi component
        comp_ver (str): dmi component version
        label (str): branch name
        base_workspace (str): path to the baseline workspace

    Return:
        (boolean): True if the workspace is pulled successfully.
                   Otherwise, returns False.
    """
    if comp_ver is None:
        # get dmi version from source tree
        with open(projlu_fullpath, 'r') as fd:
            for line in fd.readlines():
                if 'mgmt/dmi' in line:
                    dmi_version = line.replace(" ", "@")
                    dmi_version = dmi_version.strip()
                    break
    else:
        # use version in acme lschangeset
        dmi_version = comp_ver.strip()

    c_dmi_version = 'mgmt/dmi@' + label
    logger.debug("dmi_version: " + dmi_version)
    if not dmi_version.startswith(c_dmi_version):
        logger.error("Invalid ws. Cannot get dmi version.")
        return False

    logger.info('Pulling baseline ws from ' + dmi_version + '......')
    # Pull a baseline ws
    ret = run_cmd(['acme', 'init', '-comp', dmi_version, '-sb', 'binos'],
                  base_workspace)

    logger.debug('acme init: ' + ret)

    if not any("The workspace is ready for use" in s for s
               in ret.splitlines()):
        logger.error("Cannot create baseline tree.")
        return False

    return True


def trim_broken_testset(del_xpaths, tc_xpaths):
    """Trim broken test cases.

        Example:

        Match the deleted xpaths against test case using template.

        deleted xpaths:
        "/ios:native/ios:interface/ios:GigabitEthernet0/ios:name"

        test case xpath using template:
        "/ios:native/ios:interface/ios:{{ interface_name }}/ios:name"

        Add the deleted xpaths to the set of trim broken test cases
        if a match is found.

    Args:
        del_xpaths (set): deleted xpaths
        tc_xpaths (set): test case xpaths with namespace prefixes removed

    Return:
        (set): A set of broken test paths
    """
    trim_broken_tc = set()

    for del_xpath in del_xpaths:
        for tc_xpath in tc_xpaths:
            if not any(var in tc_xpath for var in var_template):
                trim_broken_tc.add(del_xpath)
                continue
            # process the template
            match = re.match(var_pattern.sub('.*', tc_xpath), del_xpath)
            if match:
                trim_broken_tc.add(del_xpath)
                break

    return trim_broken_tc


def trim_missing_testset(missing_tcs, tc_xpaths):
    """Trim missing test cases.
       Check a missing test case against the teamplate {{.*}}.

    Args:
        missing_tcs (set): missing test cases
        tc_xpaths (set): test case xpaths with namespace prefixes removed

    Return:
        (set): A set of broken test paths
    """
    trim_missing_tc = set()

    for missing_tc in missing_tcs:
        for tc_xpath in tc_xpaths:
            if not any(var in tc_xpath for var in var_template):
                continue
            # process the template
            match = re.match(var_pattern.sub('.*', tc_xpath), missing_tc)
            if match:
                break
        else:
            trim_missing_tc.add(missing_tc)

    return trim_missing_tc


def get_excluded_xpaths(workspace,
                        model_test_path,
                        modelname,
                        excluded_xpath_filename,
                        modelpath):

    """Get the list of excluded xpaths from the model directory.

    Args:
        workspace (str): path to the workspace
        model_test_path (str): path to the model test directory
        modelname (str): model name
        excluded_xpaths_filename(str): file which stores the
                                       excluded xpaths
        modelpath (str): model path

    Return:
        (set): A set of trim missing test paths
    """

    exclusion_xpaths = []
    if not modelname:
        return exclusion_xpaths

    testpath = os.path.join(workspace, model_test_path)
    excluded_path = get_excluded_xpaths_path(modelname,
                                             testpath,
                                             excluded_xpath_filename,
                                             modelpath)

    if os.path.isfile(excluded_path):
        with open(excluded_path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                exclusion_xpaths.append(line)

    return exclusion_xpaths


def remove_excluded_xpaths(trim_missing_tc,
                           modelname,
                           excluded_xpaths):
    """Remove exception xpaths from missing test cases.
       Check a missing test case against the exclusion list.

    Args:
        trim_missing_tc (set): missing test cases
        modelname (str): model name
        excluded_xpaths(list): excluded xpaths

    Return:
        (set): A set of trim missing test paths
    """
    trim_exception_tc = set()
    final_set = set()
    for xpath in excluded_xpaths:
        for missing_tc in trim_missing_tc:
            if missing_tc.startswith(xpath):
                trim_exception_tc.add(missing_tc)
    final_set = trim_missing_tc - trim_exception_tc
    return final_set


def report_excluded_xpaths(reportname,
                           trim_missing_tc,
                           modelname,
                           model_tests_path):
    """ Report missing xpaths which are not in the exclusion list.
        Exclude the missing xpaths in model_tests_path from the report

    Args:
        reportname (str): report name
        trim_missing_tc (set): missing test cases
        modelname (str): model name
        model_tests_path(list): xpaths in excluded list

    Return:
        (set): missing test cases with excluded xpaths
    """
    trim_exception_tc = set()
    if not model_tests_path:
        return trim_exception_tc

    with open(reportname, "a") as f:
        if not trim_missing_tc:
            return trim_exception_tc
        report_result('Missing test cases', f)
        report_result(17*'=', f)
        trim_exception_tc = remove_excluded_xpaths(trim_missing_tc,
                                                   modelname,
                                                   model_tests_path)
        if not trim_exception_tc:
            report_result('None', f)
        else:
            for i in trim_exception_tc:
                report_result(i, f)

        report_result('\n', f)

    return trim_exception_tc


def get_test_xpaths(tc_dict_list):
    """Retrieve test case xpaths.

    Args:
        tc_dict_list (list): a list of test case dictionaries

    Return:
        (set): A set of test case paths
    """
    tc_xpaths = set()
    for tc_dict in tc_dict_list:
        for i in tuple(tc_dict['xpaths']):
            tc_xpaths.add(i)
    return tc_xpaths


def get_tc_dict_from_xpath(xpath, tc_data_list):
    """Given an xpath, return the test case dictionary.

    Args:
        xpath (str): a xpath
        tc_dict_list (list): a list of test case dictionaries

    Return:
        (dict): A test case dictionary
    """
    found = False
    """get task directory from xpath"""
    for tc_dict in tc_data_list:
        for xp in tc_dict['xpaths']:
            if not any(var in xp for var in var_template):
                if xp == xpath:
                    found = True
                    break
                else:
                    continue
            # remove all the prefixes
            converted_xp = re.sub('[^/]+:', '', xp)
            # replace {{ interface_name }} and '_-var-_' to .*
            match = re.match(var_pattern.sub('.*', converted_xp), xpath)
            if match:
                found = True
                break

        if found:
            break

    if found:
        if 'category' in tc_dict:
            # Validate cli or oper verification
            check_tc(tc_dict)
        return tc_dict
    else:
        return None


def check_tc(tc_dict):
    """Validate if ssh verify or oper data exists given a test directory.

    Args:
        tc_dict (dict): a test case dictionary

    Return:
        None
    """
    # Build dictionary for all test cases
    # The key is the (category, task name).
    # The value is the filepath of the test case.
    tst_data = {}
    tn = tc_dict['task_name']
    cat = tc_dict['category']
    if not all_tc_dict or not (cat, tn) in all_tc_dict:
        for path, dirs, files in os.walk(os.path.join(tc_dict['path'])):
            if '__MACOSX' in path:
                continue
            for name in files:
                if name.endswith(".tst"):
                    with open(os.path.join(path, name), 'r') as f:
                        try:
                            tst_data = json.load(f)
                        except ValueError:
                            print("Invalid Test file {0}".format(name))
                    if 'tasks' in tst_data:
                        for task in tst_data['tasks']:
                            category = task[0]
                            task_name = task[1]
                            all_tc_dict[(category, task_name)] = \
                                os.path.join(path, name)

    # Look up the dict for the filepath of a test case using its category
    # and task name
    # tn = tc_dict['task_name']
    # cat = tc_dict['category']
    if (cat, tn) in all_tc_dict:
        test_filepath = all_tc_dict[(cat, tn)]
        name = os.path.basename(os.path.normpath(test_filepath))
        with open(test_filepath, 'r') as f:
            try:
                tst_data = json.load(f)
            except ValueError:
                print("Invalid Test file {0}".format(name))
            tc_dict['test_name'].add(name)
            if 'ssh' in tst_data:
                if 'verify' in tst_data.get('ssh'):
                    ssh_verify = tst_data.get('ssh').get('verify')
                    if ssh_verify:
                        tc_dict['cli_verified'] = True
            """
            if 'oper' in tst_data:
                oper_verify = tst_data.get('oper')
                if oper_verify:
                    tc_dict['oper_verified'] = True
            """


def get_rpc_tag(elem):
    """Get RPC tag, minus any XML namespace.

    Args:
        elem (element): a custom rpc element
    Return:
        tag (str): a rpc tag
    """
    if elem.tag.startswith('{'):
        return elem.tag.split('}')[1]

    return elem.tag


def build_xpaths_from_rpc(rpc, path, result):
    """Build xpaths from custome rpc.

    Args:
        rpc (str): a custom rpc
        path (str): an xpath
        result (set): a set of xpaths
    Return:
        None
    """
    for child in rpc.getchildren():
        build_xpaths_from_rpc(child, path + '/' + get_rpc_tag(child), result)

    if not len(rpc):
        result.add(path)


def process_custom_rpc(name, rpc):
    """Process custom rpc in the test case.

    Args:
        rpc (str): a custom rpc

    Return:
        result (set): a set of xpaths retrived from custom rpc
    """
    result = set()
    try:
        obj = et.fromstring(rpc)
    except et.XMLSyntaxError as e:
        logger.error("XML syntax error in rpc\n%s", str(e))
        logger.error("Please fix the test case %s", name)
        return result

    root = obj.getroottree()

    ns = 'urn:ietf:params:xml:ns:netconf:base:1.0'
    config = root.find('{%s}edit-config/{%s}config' % (ns, ns))
    if config is not None:
        build_xpaths_from_rpc(config[0],
                              '/' + get_rpc_tag(config[0]),
                              result)

    return result


def extract_zipfile(source_filename, dest_dir):
    """Extract test cases from a zip file

    Args:
        source_filename (str): zip file name
        dest_dir (dest_dir): destination directory

    Return:
        ---
    """
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)


def store_test_data(testdir):
    """Store test case data

    Args:
        testdir (str): test case directory

    Return:
        (list): List of test case dictionaries
    """
    tc_data_list = []
    tst_data = {}
    for path, dirs, files in os.walk(testdir):
        if '__MACOSX' in path:
            continue
        if 'generated' in path:
            tc_dict = process_csv_file(path, files)
            if tc_dict:
                tc_data_list.append(tc_dict)
        for name in files:
            tc_xpaths = set()
            if name.endswith(".tsk"):
                try:
                    replay = TaskHandler.get_replay(
                             os.path.dirname(path),
                             os.path.basename(path),
                             name[:name.index(".")])
                except ValueError:
                    print("Invalid Replay {0}".format(name))
                # Retrieving the xpaths
                for segment in replay.get('segments'):
                    modules = segment.get('yang').get('modules')
                    if modules is None:
                        # check for custom RPC
                        rpc = segment.get('yang').get('rpc')
                        if rpc is None:
                            continue
                        # process custom rpc
                        result = process_custom_rpc(name, rpc)
                        tc_xpaths = tc_xpaths | result
                    else:
                        for module in modules:
                            configs = modules.get(module).get('configs')
                            if configs is None:
                                continue
                            for config in configs:
                                # Strip out the list key entries
                                converted_xpath = re.sub(r"\[[^[]*]", "",
                                                         config['xpath'])
                                # Strip out namespace prefixes
                                np_xpath = re.sub('[^/]+:', '',
                                                  converted_xpath)
                                tc_xpaths.add(np_xpath)

                                # Workaround for YANG-SUITE
                                # YANG-SUITE cannot generate
                                # xpaths for list keys
                                """
                                xpth = config['xpath']
                                while xpth:
                                    if xpth.endswith(']'):
                                        opentag = xpth.rfind('[')
                                        keytag = xpth.rfind('=\"')
                                        if opentag == -1 or keytag == -1:
                                            continue
                                        keystart = opentag + 1
                                        listkey = xpth[keystart:keytag]
                                        keyxpath = os.path.join(
                                                xpth[0:opentag], listkey)
                                        # Strip out namespace prefixes
                                        nxpth1 = re.sub(r"\[[^[]*]", "", # noqa
                                                        keyxpath)
                                        nxpth = re.sub('[^/]+:', '', nxpth1)
                                        tc_xpaths.add(nxpth)
                                        xpth = xpth[:xpth.rfind('[')]
                                    else:
                                        break
                                """
                    tc_dict = dict()
                    tc_dict['task_name'] = replay.get('name')
                    tc_dict['category'] = replay.get('category')
                    # xpaths with namespace prefixes removed
                    tc_dict['xpaths'] = tc_xpaths
                    tc_dict['cli_verified'] = False
                    tc_dict['oper_verified'] = False
                    # absolute path to two levels up
                    parent_path = os.path.dirname(path)
                    tc_dict['path'] = os.path.dirname(parent_path)
                    tc_dict['test_name'] = set()

                    tc_data_list.append(tc_dict)

            if name.endswith(".tst"):
                # Get xpaths from oper test cases
                with open(os.path.join(path, name), 'r') as f:
                    try:
                        tst_data = json.load(f)
                    except ValueError:
                        print("Invalid test {0}".format(name))
                for operlist in tst_data.get('oper', []):
                    oper_opfields = operlist.get('opfields', [])
                    for op in oper_opfields:
                        if 'xpath' in op:
                            xpath1 = op.get('xpath')
                            if xpath1.startswith('//data'):
                                xpath1 = xpath1[6:]
                            else:
                                if xpath1.startswith('//'):
                                    xpath1 = xpath1[1:]
                            tc_xpaths.add(xpath1)

                if 'name' in tst_data:
                    tc_dict = dict()
                    tc_dict['task_name'] = tst_data.get('name')
                    # xpaths with namespace prefixes removed
                    tc_dict['xpaths'] = tc_xpaths
                    # absolute path to two levels up
                    parent_path = os.path.dirname(path)
                    tc_dict['path'] = os.path.dirname(parent_path)

                    tc_data_list.append(tc_dict)

            if name.endswith(".yml") or name.endswith("yaml"):
                # Get xpaths from genie yaml test cases
                if 'amt' in path:
                    continue
                tc_dict = process_mpte_tests(path, files)
                if tc_dict:
                    tc_data_list.append(tc_dict)
                break
    return tc_data_list


def process_csv_file(fpath, files):
    tc_dict = dict()
    tests_xpath = set()
    dfpath = ''
    missing_cli_verify = set()
    edit_ops = ['create', 'delete', 'remove', 'replace', 'merge']
    for name in files:
        if not name.endswith(".csv"):
            continue
        try:
            data = pd.read_csv(os.path.join(fpath, name))
            df_data = data[data['xpath'].notnull()]
            dfop = df_data.get('edit_op', '')
            if dfop:
                dfpath = df_data[df_data['edit-op'].isin(edit_ops)]
            else:
                dfpath = df_data[df_data['op'].isin(edit_ops)]
            for path in df_data.xpath:
                converted_xpath = re.sub(r"\[[^[]*]", "",
                                         path)
                # Strip out namespace prefixes
                np_xpath = re.sub('[^/]+:', '',
                                  converted_xpath)
                tests_xpath.add(np_xpath)
            if dfop:
                idx = dfpath.index[dfpath['edit-op'].isin(edit_ops)]
            else:
                idx = dfpath.index[dfpath['op'].isin(edit_ops)]
            dpath = dfpath.loc[idx]
            for index, row in dpath.iterrows():
                converted_xpath = re.sub(r"\[[^[]*]", "",
                                         str(row['xpath']))
                ns_xpath = re.sub('[^/]+:', '',
                                  converted_xpath)

                # To check if cli-verfy is in the same row as edit-op
                i = 0
                if str(row['cli-command']) != "nan" or \
                   str(row['include']) != "nan" or \
                   str(row['exclude']) != "nan" or \
                   str(row['cli-verify']) != "nan":
                    continue
                # To check if cli-verify is in the row with the test name
                elif str(row['test']) == "nan":
                    i = index - 1
                    if i < 0 or i > dpath.last_valid_index():
                        continue
                    testrows = data.iloc[i]
                    while str(testrows['test']) == "nan":
                        i = i - 1
                        if i < 0 or i > dpath.last_valid_index():
                            break
                        testrows = data.iloc[i]
                        continue
                    else:
                        if str(testrows['cli-command']) != "nan" or \
                           str(testrows['cli-verify']) != "nan" or \
                           str(testrows['include']) != "nan" or \
                           str(testrows['exclude']) != "nan":
                            continue
                        # To check if cli-verify is in the row with execute
                        # operation
                        else:
                            i = i + 1
                            if i < 0 or i > dpath.last_valid_index():
                                continue
                            testrows = data.iloc[i]
                            found = False
                            while str(testrows['test']) == "nan":
                                if str(testrows['operation']) == 'execute':
                                    if str(testrows['include']) != "nan" or \
                                       str(testrows['exclude']) != "nan":
                                        found = True
                                        break
                                    else:
                                        missing_cli_verify.add(ns_xpath)
                                        break
                                else:
                                    i = i + 1
                                    if i < 0 or i > dpath.last_valid_index():
                                        break
                                    testrows = data.iloc[i]
                                    continue
                            if not found:
                                missing_cli_verify.add(ns_xpath)
                else:
                    i = index + 1
                    if i < 0 or i > dpath.last_valid_index():
                        continue
                    testrows = data.iloc[i]
                    found = False
                    while str(testrows['test']) == "nan":
                        if str(testrows['operation']) == 'execute':
                            if str(testrows['include']) != "nan" or \
                               str(testrows['exclude']) != "nan":
                                found = True
                            else:
                                missing_cli_verify.add(ns_xpath)
                                break
                        else:
                            i = i + 1
                            if i < 0 or i > dpath.last_valid_index():
                                break
                            testrows = data.iloc[i]
                            continue
                    if not found:
                        missing_cli_verify.add(ns_xpath)
        except Exception as e:
            logger.error('Failed to prcoess the CSV file. {0}'.format(str(e)))
        tc_dict['xpaths'] = tests_xpath
        parent_path = os.path.dirname(fpath)
        tc_dict['path'] = os.path.dirname(parent_path)
        tc_dict['invalid_test'] = missing_cli_verify
        tc_dict['test_type'] = 'genie_yml'
        tc_dict['test_name'] = name
    return tc_dict


def process_mpte_tests(path, files):
    """Process the mpte genie tests to calculate the coverage"""
    tc_dict = dict()
    tc_xpaths = set()
    failed_cli = set()
    cli_verify = dict()
    file_patterns = ['mapping', 'subsection', 'testbed']
    for name in files:
        if name.endswith('yaml') or \
           name.endswith('.yml'):
            if name.startswith("data"):
                # to get the test yaml file name
                tc_dict['test_name'] = name
                with open(os.path.join(path, name), 'r') as f:
                    try:
                        tst_data = yaml.full_load(f)
                        xpaths = tst_data['data']['yang']['xpath']
                        for value in xpaths.values():
                            converted_xpath = re.sub(r"\[[^[]*]", "",
                                                     value)
                            # Strip out namespace prefixes
                            np_xpath = re.sub('[^/]+:', '',
                                              converted_xpath)
                            tc_xpaths.add(np_xpath)

                            xpth = value
                            while xpth:
                                if xpth.endswith(']'):
                                    # if 'edit-op' in config
                                    # and config['edit-op'] == 'delete':
                                    opentag = xpth.rfind('[')
                                    keytag = xpth.rfind('=\"')
                                    if opentag == -1 or keytag == -1:
                                        continue
                                    keystart = opentag + 1
                                    listkey = xpth[keystart:keytag]
                                    keyxpath = os.path.join(
                                            xpth[0:opentag], listkey)
                                    nxpth = re.sub(r"\[[^[]*]", "",
                                                   keyxpath)
                                    # Strip out namespace prefixes
                                    nxpth1 = re.sub('[^/]+:', '',
                                                    nxpth)
                                    tc_xpaths.add(nxpth1)
                                    xpth = xpth[:xpth.rfind('[')]
                                else:
                                    break

                        oper_data = tst_data['data']['yang']['returns']
                        if oper_data:
                            for key in oper_data:
                                for data in oper_data[key]:
                                    operpath = data['xpath']
                                    converted_xpath = re.sub(r"\[[^[]*]", "",
                                                             operpath)
                                    # Strip out namespace prefixes
                                    np_xpath = re.sub('[^/]+:', '',
                                                      converted_xpath)
                                    tc_xpaths.add(np_xpath)
                                    xpth = operpath
                                    # to get the xpaths for the list keys
                                    while xpth:
                                        if xpth.endswith(']'):
                                            # if 'edit-op' in config
                                            # and config['edit-op'] is
                                            # equal to 'delete'
                                            opentag = xpth.rfind('[')
                                            keytag = xpth.rfind('=\"')
                                            if opentag == -1 or keytag == -1:
                                                continue
                                            keystart = opentag + 1
                                            listkey = xpth[keystart:keytag]
                                            keyxpath = os.path.join(
                                                    xpth[0:opentag], listkey)
                                            # Strip out namespace prefixes
                                            nxpth1 = re.sub(r"\[[^[]*]", "",
                                                            keyxpath)
                                            nxpth = re.sub('[^/]+:',
                                                           '', nxpth1)
                                            tc_xpaths.add(nxpth)
                                            xpth = xpth[:xpth.rfind('[')]
                                        else:
                                            break

                    except Exception as e:
                        print(str(e))
            else:
                if not name[:name.find('_')] in \
                   file_patterns:
                    with open(os.path.join(path, name), 'r') as f:
                        try:
                            data = f.read()
                            test_data = yaml.full_load(data)
                            for key in test_data.keys():
                                if key == 'extends' or \
                                   key == 'ProfilePreconfig' or \
                                   key == 'ProfilePostconfig':
                                    continue
                                testcase = key[:key.rfind('_basic')]
                                for data in test_data[key]['test_sections']:
                                    for entry in data.keys():
                                        for action in data[entry]:
                                            if action.get('execute', ''):
                                                cli_verify = action.get(
                                                    'execute')
                                        if cli_verify:
                                            if 'include' in \
                                               cli_verify.keys() or \
                                               'exclude' in cli_verify.keys():
                                                continue
                                            else:
                                                failed_cli.add(testcase)
                        except Exception as e:
                            print(str(e))
    tc_dict['xpaths'] = tc_xpaths
    parent_path = os.path.dirname(path)
    tc_dict['path'] = os.path.dirname(parent_path)
    tc_dict['invalid_test'] = failed_cli
    tc_dict['test_type'] = 'genie_yml'
    return tc_dict


def get_zipfile_test_data(srcdir, destdir, modelname):
    """Get test data from zip file.

    Args:
        srcdir (str): zip file soruce directory
        destdir (str): directory to extract the zip file
        modelname (str): model name

    Return:
        (bool, bool): True if zip file exists. Otherwise, return False
                      True if errors are found
    """
    found = False
    error = False
    # fname = ''
    for path, dirs, files in os.walk(srcdir):
        if '__MACOSX' in path:
            continue
        for name in files:
            if zipfile.is_zipfile(os.path.join(path, name)):
                extract_path = os.path.join(destdir, modelname, name)
                if not os.path.exists(extract_path):
                    try:
                        os.makedirs(extract_path)
                    except OSError:
                        error = True
                        logger.error("Failed to create directory for zip "
                                     "files")
                        break
                extract_zipfile(os.path.join(path, name), extract_path)
                found = True

    return found, error


def get_test_data(model_tests_fullpath, modelpath, modelname, zipfdir):
    """Scan through the test case directories in ws.
       Store task details in a dictionary.

    Args:
        model_tests_fullpath (str): full path to model test cases in a ws
        modelist (list): a list of model names
        zipfdir (str): zip file temp directory

        Example:
        model_tests_fullpath:
        '/nobackup/graceho/polaris_dev/git/0919/polaris/'
        'binos/mgmt/dmi/model/tests'
        modellist:
        [('/mgmt/dmi/libyang/_gen_yang-src-x86_64_cge7-vxe',
          'Cisco-IOS-XE-bgp-oper')]
        zipfdir
        '/tmp/tmpy47uyfbg/zip_tmpdir'

    Return:
        (list, bool): A list of test case dictionaries and a bool to indicate
                      if errors are found
    """
    tc_data_list = []

    # test_model_subdir: 'ned' or 'openconfig' or 'tdl-oper'
    test_model_subdir = get_model_subdir(modelname, modelpath)
    # test_model_fullpath:
    # i.e. <ws>/binos/mgmt/dmi/model/tests/ned/Cisco-IOS-XE-cdp
    test_model_fullpath = os.path.join(model_tests_fullpath,
                                       test_model_subdir,
                                       modelname)

    tc_data_list = store_test_data(test_model_fullpath)

    found, error = get_zipfile_test_data(test_model_fullpath,
                                         zipfdir,
                                         modelname)
    if found and not error:
        # Store test cases from zip file
        zipfile_data_list = store_test_data(os.path.join(
                                            zipfdir, modelname))
        tc_data_list += zipfile_data_list

    return tc_data_list, error


def find_tdlmodel(workspace, mn):
    """Find tdl model.

    Args:
        workspace (str): Path to the workspace
        mn (str): model name

    Return:
        (str): model path
    """
    # Find the tdl model. Return the path.
    libyangdir = [x[0] for x in
                  os.walk(os.path.join(workspace,
                                       'binos',
                                       'mgmt/dmi/libyang'))]
    for path in libyangdir:
        # Look for all tdl models in mgmt/dmi/libyang/_gen_yang-src*
        if 'mgmt/dmi/libyang/_gen_yang-src' in path:
            # Copy only .yang files
            files = glob.iglob(os.path.join(path, "*.yang"))
            for f in files:
                if mn in f:
                    return path.strip().split('binos')[-1].lstrip('/')

    return ""


def strip_tdlmodelpath():
    """Strip tdl model path.

    Return:
        (str): model path
    """
    return TDLMODELPATH.lstrip('/')


def get_model_subdir(modelname, modelpath):
    """Get model subdirectory.

    Args:
        modelname (str): Name of the model
        modelpath (str): model path

    Return:
        (str): type of model
    """
    if strip_tdlmodelpath() in modelpath:
        return "tdl-oper"

    if modelname.startswith('Cisco-IOS-XE'):
        return "ned"

    if "openconfig" in modelname:
        return "openconfig"

    return ''


def get_excluded_xpaths_path(modelname,
                             model_tests_fullpath,
                             excluded_xpaths_filename,
                             modelpath):
    """Get the location of the excluded xpaths file in a workspace.

    Args:
        modelname (str): model name
        model_tests_fullpath (str): path to the model test directory
        excluded_xpaths_filename(str): name of the file which contains the
                                       excluded xpaths

    Return:
        (str): path to the excluded xpaths file
    """

    test_model_subdir = get_model_subdir(modelname, modelpath)
    excluded_xpaths_path = os.path.join(model_tests_fullpath,
                                        test_model_subdir,
                                        modelname,
                                        excluded_xpaths_filename)

    return excluded_xpaths_path


def create_git_ws(chgsetfile, workspace, model_path,
                  label, base_workspace, modelnames):
    """Create a git ws.

    Args:
        chgsetfile (str): temp file contains the list of modified models
        workspace (str): user workspace
        model_path (str): model directory in ws
        label (str): branch name
        base_workspace (str): baseline workspace
        modelnames (str): Path to file contains list of modified models

        Example:
        chgsetfile: '/tmp/tmp1_xx_p_s/changeset.txt'
        workspace: '/nobackup/graceho/polaris_dev/git/0919/polaris'
        model_path: 'mgmt/dmi/model/yang/src'
        label: polaris_dev
        base_workspace: '/tmp/tmp1_xx_p_s/base_workspace'
        modelnames: None

    Return:
        (set): a set of modified models
    """
    modelist = list()
    newmodel = list()
    if not modelnames:
        # No model list pass in
        ret = get_git_changeset(chgsetfile,
                                os.path.join(workspace,
                                             'binos',
                                             model_path))
        if ret:
            logger.error("Unable to get changeset")
            return modelist, newmodel

    # Step 1: Copy the reference models i.e. ned, openconfig
    # src: /nobackup/graceho/polaris_dev/git/0912/polaris/ +
    #      binos/mgmt/dmi/model/yang/src
    # dst: /tmp/tmpf5hotcqw/base_workspace/mgmt/dmi/model/yang/src
    src = os.path.join(workspace, 'binos', model_path)
    dst = os.path.join(base_workspace, model_path)
    # copy the tree
    shutil.copytree(src, dst)

    # Step 2: Copy the reference tdl models
    # Loop through directory
    # /nobackup/graceho/polaris_dev/git/0912/polaris/binos/ +
    # mgmt/dmi/libyang
    """
    libyangdir = [x[0] for x in
                  os.walk(os.path.join(workspace,
                                       'binos',
                                       'mgmt/dmi/libyang'))]
    tdl_model_path = os.path.join(strip_tdlmodelpath(), 'model')
    tdldst = os.path.join(base_workspace, tdl_model_path)

    # tdldst: /tmp/tmp1_xx_p_s/base_workspace/mgmt/dmi/libyang/model
    os.makedirs(tdldst)

    for path in libyangdir:
        # Look for all tdl models in mgmt/dmi/libyang/_gen_yang-src*
        if 'mgmt/dmi/libyang/_gen_yang-src' in path:
            # Copy only .yang files
            files = glob.iglob(os.path.join(path, "*.yang"))
            for f in files:
                if os.path.isfile(f):
                    shutil.copy2(f, tdldst)
    """
    # copy the baseline models
    if not modelnames:
        filepath = chgsetfile
    else:
        filepath = modelnames
    patterns = ['cisco-xe', 'oper.yang', 'transform.yang', '-ann.yang', '-deviation.yang', '.json']
    ignore = False
    with open(filepath, 'r') as f:
        for line in f.readlines():
            line = line.strip().split('binos')
            line = 'binos' + line[-1]
            if line.endswith('.yang') and any(md in line for md in MODELDIRS):
                # When there is a change in transform file
                """
                if line.endswith('transform.yang'):
                    line = line.replace('-transform', '')
                    copy_tdl_base_model(line, workspace, base_workspace)
                """
                if any(pattern in line for pattern in patterns):
                    ignore = True
                    continue
                else:
                    # Note: For NED and openconfig model
                    ret = copy_base_model(line, workspace,
                                          label, base_workspace)
                    if ret:
                        logger.error('Unable to copy base model ', line)
                        logger.info('No base version found.' +
                                    ' {0} is a new model'.format(line))
                        change_path = os.path.splitext(line)[0]
                        modelpath = os.path.dirname(change_path)
                        modelname = os.path.basename(change_path)
                        newmodel.append((modelpath, modelname))
                        continue
                # change_path:
                # 'binos/mgmt/dmi/libyang/src/yang/Cisco-IOS-XE-bgp-oper'
                change_path = os.path.splitext(line)[0]
                # Path to the model
                # modelpath: 'binos/mgmt/dmi/libyang/src/yang'
                modelpath = os.path.dirname(change_path)
                # modelname: 'Cisco-IOS-XE-bgp-oper'
                modelname = os.path.basename(change_path)
                modelist.append((modelpath, modelname))
            else:
                ignore = True
    if ignore and not modelist and not newmodel:
        return ['success'], newmodel
    return modelist, newmodel


def create_acme_ws(chgsetfile, workspace, model_path,
                   label, base_workspace, precommit_tmpdir):
    """Create an acme ws.

    Args:
        chgsetfile (str): temp file contains the list of modified models
        workspace (str): user workspace
        model_path (str): model directory in ws
        label (str): branch name
        base_workspace (str): baseline workspace
        precommit_tmpdir (str): precommit temporary directory

    Return:
        (list): a list of tuples (model path, modified model name)
    """
    modelist = list()
    projlu_path = 'binos/.acme_project/proj.lu'

    # Get changeset
    chgset_version = get_acme_changeset(chgsetfile,
                                        os.path.join(workspace,
                                                     'binos',
                                                     model_path))

    # Pull baseline ws
    if not pull_baseline_acme_ws(os.path.join(workspace, projlu_path),
                                 chgset_version,
                                 label,
                                 base_workspace):
        shutil.rmtree(precommit_tmpdir)
        return modelist

    # xpath processing
    logger.info("Processing xpaths......")

    plist = ['M', 'A']
    with open(chgsetfile, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line[0] in plist and line.endswith('.yang'):
                fullpath = line[3:]
                filename = os.path.basename(fullpath)
                modelname = os.path.splitext(filename)[0]
                modelpath = 'binos/mgmt/dmi'
                modelpath += fullpath.split(filename)[0].rstrip('/')
                modelist.append((modelpath, modelname))

    return modelist


def create_baseline_ws(chgsetfile, workspace, model_path,
                       label, base_workspace, precommit_tmpdir, modelnames):
    """Create baseline ws.

    Args:
        chgsetfile (str): temp file contains the list of modified models
        workspace (str): user workspace
        model_path (str): model directory in ws
        label (str): branch name
        base_workspace (str): baseline workspace
        precommit_tmpdir (str): precommit temporary directory
        modelnames (str): Path to file contains list of modified models

    Return:
        (set): a set of modified models
    """
    newmodel = list()
    """
    if (os.path.isdir(os.path.join(workspace, ".git"))):
        modelist, newmodel = create_git_ws(
                chgsetfile, workspace, model_path,
                label, base_workspace, modelnames)
    else:
        modelist = create_acme_ws(chgsetfile, workspace,
                                  model_path, label,
                                  base_workspace,
                                  precommit_tmpdir)
    """
    modelist, newmodel = create_git_ws(
            chgsetfile, workspace, model_path,
            label, base_workspace, modelnames)

    return modelist, newmodel


def is_data_node(entry):
    """Validate if this is a data node.

    Args:
        entry (list): an entry

    Return:
        (boolean): True if entry is a data node
    """
    # Check for presence container
    lentry = len(entry)
    if lentry >= 5 and entry[3] == 'container' and entry[4] == 'true':
        return True
    else:
        return entry[3] not in [
            'case',
            'choice',
            'container',
            'grouping',
            'identity',
            'typedef',
            'input',
            'output',
        ]


def get_all_xpaths(workspace, model_path, fset):
    """Get all xpaths from a model.

    Args:
        workspace (str): path to a ws
        model_path (list): model directory in ws
        fset (set): model name

    Return:
        (set): a set of xpaths
        (bool): True if it is a submodule
                Otherwise, return False
    """
    addons = ['status', 'module', 'nodetype', 'presence', 'deviation', 'key']

    new_xpaths = set()
    obsolete_containers = set()
    not_supported_containers = set()
    remove_obsolete_xpaths = set()
    filter_new_xpaths = set()
    for modelname in fset:
        model_subdir = get_model_subdir(modelname, model_path)

        if not model_subdir:
            logger.info('Model: ' + modelname + 'not supported')
            continue

        if model_subdir == "tdl-oper":
            # TDL generated model.
            model_subdir = ""

        to_dataset = dataset_for_directory(
            os.path.join(workspace,
                         'binos',
                         model_path.lstrip('/'),
                         model_subdir),
            modelname,
            addons
        )

        is_submod = False
        for row in to_dataset['data']:
            if not is_submod and row[-1] == 'submodule':
                is_submod = True
            # Filter out obsolete nodes
            if row[1] == 'obsolete':
                if row[3] in ['container', 'list']:
                    trim_obsolete_xpath = re.sub('[^/]+.:', '', row[0])
                    obsolete_containers.add(trim_obsolete_xpath)
                continue
            # Filter out not supported nodes
            if row[5] == 'not-supported':
                if row[3] in ['container', 'list']:
                    trim_not_supported_xpath = re.sub('[^/]+.:', '', row[0])
                    not_supported_containers.add(trim_not_supported_xpath)
                    continue
            if not is_data_node(row):
                continue
            # Filter out not supported leaf nodes
            if row[5] == 'not-supported':
                continue
            if row[6]:
                continue
            converted_new_xpath = re.sub('[^/]+.:', '', row[0])
            new_xpaths.add(converted_new_xpath)

    # This is a check added to catch those models which are not
    # following RFC standard for obsolete nodes
    # Filter out all xpaths whose parents are marked absolete
    for obsolete_container in obsolete_containers:
        for new_xpath in new_xpaths:
            if new_xpath.startswith(obsolete_container + '/'):
                remove_obsolete_xpaths.add(new_xpath)

    # Filter out all the not supported xpaths whose parents
    # are marked not-supported in the 'deviation' field
    for not_supported_container in not_supported_containers:
        for new_xpath in new_xpaths:
            if new_xpath.startswith(not_supported_container + '/'):
                continue
            else:
                filter_new_xpaths.add(new_xpath)
    else:
        filter_new_xpaths = new_xpaths

    new_xpaths = filter_new_xpaths - remove_obsolete_xpaths
    return new_xpaths, remove_obsolete_xpaths, is_submod


def get_changed_xpaths(workspace, modelpath, base_workspace, modelname):
    """Get changed xpaths from ws.

    Args:
        workspace (str): path to a ws
        model_path (list): model directory in ws
        base_workspace: path to a baseline ws
        fset (set): a set of model names

    Return:
        new_xpaths (set): a set of newly added xpaths
        del_xpaths (set): a set of deleted xpaths
    """
    addons = ['datatype', 'module',
              'min', 'max', 'must',
              'when', 'presence', 'status', 'key', 'nodetype']

    new_xpaths = set()
    del_xpaths = set()
    mod_xpaths = set()
    obsolete_xpaths = set()
    model_subdir = get_model_subdir(modelname, modelpath)

    if not model_subdir:
        logger.info('Model: ' + modelname + 'not supported')
        return new_xpaths, del_xpaths, mod_xpaths, False

    if model_subdir == "tdl-oper":
        # tdl generated model
        model_subdir = ""
        model_path_base = os.path.join(strip_tdlmodelpath(), 'model')
        # model_path_current:
        # 'mgmt/dmi/libyang/_gen_yang-src-x86_64_cge7-vxe'
        model_path_current = find_tdlmodel(workspace, modelname)
    else:
        if 'binos' in modelpath:
            modelpath = modelpath[modelpath.find('/'):].strip('/')
        model_path_base = modelpath
        model_path_current = modelpath

    # /tmp/tmpf5hotcqw/base_workspace/mgmt/dmi/model/yang/src/ned
    from_dataset = dataset_for_directory(
        os.path.join(base_workspace,
                     model_path_base),
        modelname,
        addons
    )

    to_dataset = dataset_for_directory(
        os.path.join(workspace,
                     'binos',
                     model_path_current),
        modelname,
        addons
    )
    is_submod = False
    for row in to_dataset['data']:
        if not is_submod and row[-1] == 'submodule':
            is_submod = True

    dscmp = getdiff(from_dataset, to_dataset)

    for row in dscmp['data']:
        converted_new_xpath = re.sub('[^/]+.:', '', row[1])
        if row[11] == 'container' and row[8] != 'true':
            continue
        if row[11] == 'list':
            continue
        if row[10] == 'true':
            continue
        if row[0] == '+':
            new_xpaths.add(converted_new_xpath)

        if row[0] == '-':
            del_xpaths.add(converted_new_xpath)

        if row[0] == '>' and row[9] != 'obsolete':
            mod_xpaths.add(converted_new_xpath)

        if row[9] == 'obsolete':
            obsolete_xpaths.add(converted_new_xpath)

    return new_xpaths, del_xpaths, mod_xpaths, obsolete_xpaths, is_submod


def report_new_xpaths(reportname, new_xpaths, mod_xpaths, tdl):
    """Report newly added xpaths.

    Args:
        reportname (str): report name
        new_xpaths (set): a set of newly added xpaths
        tdl (list): a list of test case directories

    Return:
        missing_cli (boolean): True if no cli is defined.
                               Otherwise, return False
        missing_cli_verify (boolean): True if cli verification is not defined.
                                      Otherwise, return False.
    """
    invalid_testcase = set()
    cli_dict = {}
    all_xpaths = set()
    missing_tc = set()
    with open(reportname, "a") as f:
        report_result('\nNew xpaths', f)
        report_result('==========', f)
        for i in new_xpaths:
            all_xpaths.add(i)
            report_result(i, f)
        report_result('\nModified xpaths', f)
        report_result('===============', f)
        for i in mod_xpaths:
            all_xpaths.add(i)
            report_result(i, f)
        missing_cli = False
        missing_cli_verify = False
        for i in all_xpaths:
            tc_dict = get_tc_dict_from_xpath(i, tdl)
            if not tc_dict:
                missing_cli = True
                missing_tc.add(i)

            else:
                if 'cli_verified' in tc_dict and not tc_dict['cli_verified']:
                    missing_cli_verify = True
                    if tc_dict['test_name']:
                        cli_dict[i] = str(tc_dict['test_name'])
                        report_result('  \nWARNING: MISSING CLI Verification ' +
                                      str(tc_dict['test_name']), f)
                    else:
                        cli_dict[i] = str(tc_dict['task_name'])
                        report_result('  \nWARNING: MISSING CLI Verification ' +
                                      '  task(s): ' + str(tc_dict['task_name']), f)
                    report_result(i, f)
        if missing_tc:
            report_result("\nMISSING TEST CASES", f)
            report_result("\n==================", f)
            for i in missing_tc:
                report_result(i, f)
        if not all_xpaths:
            report_result('None', f)
        if cli_dict:
            for key in cli_dict.keys():
                invalid_testcase.add(key)
        report_result('\n', f)

    return missing_cli, \
        missing_cli_verify, \
        invalid_testcase


def report_deleted_xpaths(reportname, del_xpaths):
    """Report deleted xpaths.

    Args:
        reportname (str): report name
        del_xpaths (set): a set of deleted xpaths

    Return:
        None
    """
    with open(reportname, "a") as f:
        report_result('Removed xpaths', f)
        report_result('==============', f)
        if not del_xpaths:
            report_result('None', f)
        else:
            for i in del_xpaths:
                report_result(i, f)

        report_result('\n', f)


def report_missing_xpaths(reportname, new_xpaths,
                          tc_xpaths,
                          excluded_xpaths,
                          is_submod):
    """ Report missing xpaths.

    Args:
        reportname (str): report name
        new_xpaths (set): a set of newly added xpaths
        tc_xpaths (list): a set of test case xpaths
        is_submod (bool): True if it is a submodule
                          Otherwise, set to False

    Return:
        (bool): True if missing test case exists
                Otherwise, returns False
    """

    missing_tc = set()
    trim_missing_tc = set()
    if is_submod:
        # process xpaths from submodule
        for new_xpath in new_xpaths:
            if not any(new_xpath in tc_xpath for tc_xpath in tc_xpaths):
                missing_tc.add(new_xpath)
    else:
        missing_tc = new_xpaths - tc_xpaths
    trim_missing_tc = trim_missing_testset(missing_tc, tc_xpaths)

    if excluded_xpaths:
        return trim_missing_tc

    with open(reportname, "a") as f:
        report_result('Missing test cases', f)
        report_result('==================', f)
        if not missing_tc:
            report_result('None', f)
        else:
            if not trim_missing_tc:
                report_result('None', f)
            else:
                for i in trim_missing_tc:
                    report_result(i, f)

        report_result('\n', f)

    return trim_missing_tc


def report_broken_xpaths(reportname, del_xpaths, tc_xpaths):
    """Report broken xpaths.

    Args:
        reportname (str): report name
        del_xpaths (set): a set of deleted xpaths
        tc_xpaths (list): a set of test case xpaths

    Return:
        (boolean): True if broken test case exists.
                   Otherwise, returns False.
    """
    with open(reportname, "a") as f:
        trim_broken_tc = trim_broken_testset(del_xpaths, tc_xpaths)
        report_result('Broken test cases', f)
        report_result('==================', f)
        if not trim_broken_tc:
            report_result('None', f)
        else:
            for i in trim_broken_tc:
                report_result(i, f)

        report_result('\n', f)

    if (len(trim_broken_tc) > 0):
        return True

    return False


def report_obsolete_xpaths(reportname, obsolete_xpaths):
    """Report obsolete xpaths.

    Args:
        reportname (str): report name
        obsolete_xpaths (set): a set of obsolete xpaths

    Return:
        None
    """
    if not obsolete_xpaths:
        return
    with open(reportname, "a") as f:
        report_result('Below xpaths should mark obsolete in the model', f)
        report_result(46*'=', f)
        for i in obsolete_xpaths:
            report_result(i, f)

        report_result('\n', f)

    return


def report_invalid_testcases(reportname,
                             obsolete_xpaths,
                             tc_xpaths,
                             tdl,
                             excluded_xpaths):
    """Report invalid testcases.

    Args:
        reportname (str): report name
        obsolete_xpaths (set): a set of obsolete xpaths
        tc_xpaths (set): a set of test case xpaths
        tdl (list): a list of test case directories
        excluded_xpaths (set): excluded_xpaths

    Return:
        (set): invalid test cases which are part of the excluded xpaths
    """
    invalid_tc_no_exception = set()
    invalid_tc_with_exception = set()
    invalid_testcase = set()
    for xpath in excluded_xpaths:
        for tc_xpath in tc_xpaths:
            if tc_xpath.startswith(xpath):
                invalid_tc_with_exception.add(tc_xpath)

    invalid_tc_no_exception = tc_xpaths - invalid_tc_with_exception

    obsolete_dict = dict()
    cli_dict = dict()
    oper_dict = dict()

    for i in invalid_tc_no_exception:
        tc_dict = get_tc_dict_from_xpath(i, tdl)
        if not tc_dict:
            continue
        if tc_dict.get('test_type', '') == 'genie_yml':
            if tc_dict['invalid_test']:
                for tests in tc_dict['invalid_test']:
                    invalid_testcase.add(tests)
        if i in obsolete_xpaths:
            if tc_dict['test_name']:
                obsolete_dict[i] = str(tc_dict['test_name'])
            else:
                obsolete_dict[i] = str(tc_dict['task_name'])
        else:
            if 'cli_verified' in tc_dict and not tc_dict['cli_verified']:
                if tc_dict['test_name']:
                    cli_dict[i] = str(tc_dict['test_name'])
                else:
                    cli_dict[i] = str(tc_dict['task_name'])

            if 'oper_verified' in tc_dict and not tc_dict['oper_verified']:
                if tc_dict['test_name']:
                    oper_dict[i] = str(tc_dict['test_name'])
                else:
                    oper_dict[i] = str(tc_dict['task_name'])

    with open(reportname, "a") as f:
        if obsolete_dict or cli_dict or oper_dict:
            report_result('Invalid/Incomplete test cases', f)
            report_result(30*'=' + '\n', f)
        if cli_dict:
            for key in cli_dict.keys():
                invalid_testcase.add(key)
        msg = 'OBSOLETE test cases'
        print_invalid_testcases(obsolete_dict, msg, f)

        # msg = 'MISSING CLI Verification'
        # print_invalid_testcases(cli_dict, msg, f)

        msg = 'MISSING Operational Verification'
        # print_invalid_testcases(oper_dict, msg, f)

    return invalid_tc_with_exception, invalid_testcase


def calculate_test_coverage(reportname,
                            total_xpaths,
                            tc_xpaths,
                            missing_tc,
                            exception_tc,
                            exception_list,
                            invalid_testcase,
                            failed_tc):
    """Calculate test coverage.

    Args:
        reportname (str): report name
        total_xpaths (set): all xpaths
        missing_tc (set): missing test cases
        exception_tc (set): missing test cases that are not part of the
                            excluded xpaths
        exception_list (list): excluded xpaths
        invalid_testcase (set): invalid testcases which are part of the
                                excluded xpaths

    Return:
        ---
    """
    result = {}
    with open(reportname, "a") as f:
        if total_xpaths:
            test_coverage = ((len(total_xpaths) -
                              (len(missing_tc) +
                               len(failed_tc))) / len(total_xpaths))
            if exception_list:
                with_exception = ((len(total_xpaths) -
                                  (len(exception_tc)+len(failed_tc))) /
                                  len(total_xpaths))

                # report_result('Test Coverage (no paths excluded): ' +
                #        '{:.1%}\n'.format(test_coverage), f)
                """
                report_result('Excluding xpaths', f)
                report_result(16*'=', f)
                for exception_xpath in exception_list:
                    report_result(exception_xpath, f)
                """
                # test_coverage = with_exception

                if invalid_testcase:
                    report_result('\nInvalid/Incomplete test cases ' +
                                  'that are part of excluded paths ' +
                                  '(please remove these tests)', f)
                    report_result(90*'=', f)
                    for invalid_tc in invalid_testcase:
                        report_result(invalid_tc, f)

                    report_result('\n', f)
            else:
                with_exception = test_coverage
            print("\n")
            if tc_xpaths:
                report_result('\n Xpaths with test cases', f)
                report_result(45*'=', f)
                for tc in tc_xpaths:
                    report_result(tc, f)
                report_result('\n', f)
            if missing_tc:
                report_result('\nXpaths missing test cases before exclusion', f)
                report_result(45*'=', f)
                for tc in missing_tc:
                    report_result(tc, f)
                report_result('\n', f)
            if failed_tc:
                report_result('\nFollowing xpaths are missing cli ' +
                              'verification', f)
                report_result(45*'=', f)
                for tc in failed_tc:
                    report_result(tc, f)
                report_result('\n', f)
            print("Total xpaths in the model: {0}".format(
                  len(total_xpaths)))
            if exception_tc:
                print("Number of xpaths missing test cases " +
                      "after exclusion: {0}".format(len(exception_tc)))
            print("Total no of Xpaths missing test cases: {0}".format(
                  len(missing_tc)))
            print("Xpaths without cli-verification: {0}".format(
                  len(failed_tc)))
            print("\n")
            report_result('Test Coverage (no paths excluded): ' +
                          '{:.1%}\n'.format(test_coverage), f)
            report_result('Test Coverage: {:.1%}'.format(with_exception), f)

            report_result('\n', f)
            result['total_xpaths'] = len(total_xpaths)
            result['missing_tc'] = len(missing_tc)
            result['missing_cliverify'] = len(failed_tc)
            result['coverage_exclusion'] = '{:.1%}'.format(with_exception)
            result['coverage_percentage'] = '{:.1%}'.format(test_coverage)
            """
            if (test_coverage and with_exception) != '100.0%':
                result['status'] = 'failed'
            else:
                result['status'] = 'passed'
            """


class TaskFetchError(Exception):
    pass


class TaskPublishError(Exception):
    pass


def print_precommit_report_result(reportname, missing_tc,
                                  missing_cli, broken_tc,
                                  missing_cli_verify):
    """Print precommit report.

    Args:
        reportname (str): report name
        missing_tc (boolean): True if missing test cases are found.
                                   Otherwise, this is set to False.
        missing_cli (boolean): True if no cli is found in test case.
                               Otherwise, this is set to False.
        broken_tc (boolean): True if broken test cases are found.
                                  Otherwise, this is set to False.
        missing_cli_verify (boolean): True if missing cli verification.
                                      Otherwise, this is set to False.
    Return:
        ---
    """
    with open(reportname, "a") as f:
        # Report PASS or FAIL
        if (missing_tc or missing_cli or broken_tc or
                missing_cli_verify):
            report_result('PRECOMMIT FAILED', f)
            report_result('-----------------', f)
            if missing_tc or missing_cli:
                report_result('MISSING TESTCASES', f)
            if broken_tc:
                report_result('BROKEN TESTCASES', f)
            if missing_cli_verify:
                report_result('MISSING CLI VERIFICATION', f)
        else:
            report_result('PRECOMMIT SUCCESS\n', f)


def add_cdets_enclosure(reportname, bugid, label, title):
    """Add enclosure to cdets.

    Args:
        reportname (str): report name
        bugid (str): bug id
        label (str): branch name
        title (str): enclosure title

    Return:
        ---
    """

    if bugid:
        logger.info('Adding ned precommit result to ' + bugid)
        logger.info('Please wait.......')
        # timestamp = datetime.datetime.utcnow().strftime("%y%m%d-%H%M%S")
        # enclosure_prefix = title + label + '-' + timestamp

        # write results to DDTS
        ret = run_cmd(['/usr/cisco/bin/addfile',
                       '-o',
                       bugid,
                       title,
                       reportname])
        print('Done: ' + ret)


def save_log(full_report, logfile):
    """Save the log.

    Args:
       full_report (string): Path to the full log
       logfile (string): Path to copy the log file to

    """

    if full_report is None or logfile is None:
        return

    if not os.path.isfile(full_report):
        # Create an empty file if not exists
        open(full_report, 'a').close()

    if os.path.exists(os.path.dirname(logfile)):
        # Copy the file
        shutil.copyfile(full_report, logfile)


def turn_on_console_log(logfile):
    """Turn on console log.

    Args:
       logfile (string): Path to the logfile
    """
    global console_log

    if not logfile:
        console_log = True


def copy_ned_models(workspace, tmpdir):
    """ Copy ned model from workspace to tmpdir """
    try:
        modeldir = 'binos/mgmt/dmi/model/yang/src/ned'
        srcpath = os.path.join(workspace, modeldir)
        full_dest_path = os.path.join(tmpdir, modeldir)
        shutil.copytree(srcpath, full_dest_path)
    except OSError:
        pass

    #
    # remove the files that shouldn't be there
    #
    to_remove = [
        'Cisco-IOS-XE-CEDGE-*.yang'
        ]

    for p in to_remove:
        files_to_removed = glob.glob('%s/%s' % (full_dest_path, p))
        for f in files_to_removed:
            try:
                os.remove(f)
            except OSError:
                pass
        map(os.remove, glob.glob('%s/%s' % (full_dest_path, p)))

    return full_dest_path


def precommit_check(workspace=None,
                    label=None,
                    reportname=None,
                    bugid=None,
                    report=None,
                    logfile=None,
                    modelpath=None,
                    modelnames=None):
    """Precommit check entry point.
       This is called by model coverage script, precommit
       script and paw_wrapper script.

       Input parameters for model coverage script:
         workspace (mandatory)
         label (mandatory)
         bugid (optional)
         logfile (optional)

       Input parameters for precommit script:
         workspace (mandatory)
         label (mandatory)
         reportname (mandatory)
         report (mandatory)
         logfile (optional)
         modelnames (optional)
         modelpath (optional)

       paw_wrapper script also calls this function to perform model coverage.

    Args:
       workspace (string): Workspace
       label (string): Branch name
       reportname: (string): Report name
       bugid: (string): DDTS number
       report (boolean): True if generated the report for the model
                         Otherwise, it is set to False
       logfile (string): Path to copy the log file to
       modelnames (string): Path to file contains list of modified models
       modelpath (string): Path to generated models

    """
    if not workspace:
        ws = input('Full directory path to your workspace: ')
        workspace = ws
    if not label:
        lbl = input('Workspace label: ')
        label = lbl
    """
    if not bugid:
        bid = input('bugid: ')
        bugid = bid
    """
    # Generate code coverage report
    if report:
        if not reportname:
            reportname = input('Enter model name: ')
            if not reportname:
                logger.error("No model name specified")
                return
        """
        if not modelpath:
            modelpath = input('Model path: ')
            modelpath = modelpath.rstrip()
        """
    # Turn on console log if no log file is specified
    turn_on_console_log(logfile)

    excluded_xpath_filename = 'excluded_xpaths'
    if not modelpath:
        # Set model path
        modelpath = 'mgmt/dmi/model/yang/src'
    else:
        tdl_modelpath = TDLMODELPATH.lstrip('/')
        if tdl_modelpath not in modelpath:
            modelpath = 'mgmt/dmi/model/yang/src'
    model_test_path = 'binos/mgmt/dmi/model/tests'
    # Set up directories and paths
    precommit_tmpdir = tempfile.mkdtemp()
    # File to store for precommit result
    full_report = os.path.join(precommit_tmpdir, 'full_report.txt')
    # Create top directory for zip files
    zipfile_path = os.path.join(precommit_tmpdir, 'zip_tmpdir')
    os.mkdir(zipfile_path)
    modelist = list()
    result = {}
    err_msg = []
    no_changes = False
    changed_xpaths = set()
    rem_item = set()
    newmodel = set()

    if not reportname:
        chgsetfile = os.path.join(precommit_tmpdir, 'changeset.txt')
        # directory holding base models to compare against
        base_workspace = os.path.join(precommit_tmpdir, 'base_workspace')
        os.mkdir(base_workspace)

    try:
        is_submod = False
        if not reportname:
            modelist, newmodel = create_baseline_ws(
                    chgsetfile, workspace,
                    modelpath, label, base_workspace,
                    precommit_tmpdir, modelnames)
            if not modelist and not newmodel:
                if console_log:
                    logger.warning("Empty model set")
                else:
                    save_log(full_report, logfile)
                return True
            if not modelist and not newmodel:
                save_log(full_report, logfile)
                result['status'] = 'failure'
                err_msg.append('No Model changes detected')
                return
            elif newmodel:
                for model_path, modelname in newmodel:
                    if "libyang" in model_path:
                        no_changes = True
                        continue
                    fset = []
                    fset.append(modelname)
                    test_model_subdir = get_model_subdir(modelname, modelpath)
                    if "ned" in test_model_subdir:
                        # full_dst_pth = copy_ned_models(workspace, precommit_tmpdir)
                        all_xpaths, obsolete_xpaths, is_submod = get_all_xpaths(precommit_tmpdir,
                                                                                modelpath,
                                                                                fset)
                    else:
                        all_xpaths, obsolete_xpaths, is_submod = get_all_xpaths(workspace,
                                                                                modelpath,
                                                                                fset)
                    tdl, error = get_test_data(os.path.join(workspace, model_test_path),
                                               model_path,
                                               modelname,
                                               zipfile_path)
                    if error:
                        # Unable to retrieve test data
                        return False
                    tc_xpaths = get_test_xpaths(tdl)
                    with open(full_report, 'a') as fd:
                        report_result('\nModel: {0}'.format(modelname), fd)
                        report_result('=================================', fd)
                    invalid_testcase = set()
                    excluded_xpaths = get_excluded_xpaths(workspace,
                                                          model_test_path,
                                                          modelname,
                                                          excluded_xpath_filename,
                                                          model_path)

            for model_path, modelname in modelist:
                if "libyang" in model_path:
                    no_changes = True
                    continue
                all_xpaths = set()
                new_xpaths, del_xpaths, mod_paths, obs_paths, is_submod = get_changed_xpaths(
                    workspace,
                    model_path,
                    base_workspace,
                    modelname)
                if not new_xpaths and not mod_paths:
                    rem_item.add((model_path, modelname))
                    if not changed_xpaths:
                        no_changes = True
                    continue
                else:
                    if no_changes:
                        no_changes = False
                all_xpaths = new_xpaths.union(mod_paths)
                if all_xpaths:
                    changed_xpaths = all_xpaths
                tdl, error = get_test_data(os.path.join(workspace, model_test_path),
                                           model_path,
                                           modelname,
                                           zipfile_path)
                if error:
                    # Unable to retrieve test data
                    return False
                tc_xpaths = get_test_xpaths(tdl)
                with open(full_report, 'a') as fd:
                    report_result('\nModel: {0}'.format(modelname), fd)
                    report_result('=================================', fd)
                no_cli, no_cliver, failed_tc = report_new_xpaths(full_report,
                                                                 new_xpaths,
                                                                 mod_paths,
                                                                 tdl)
                report_deleted_xpaths(full_report, del_xpaths)

                excluded_xpaths = get_excluded_xpaths(workspace,
                                                      model_test_path,
                                                      modelname,
                                                      excluded_xpath_filename,
                                                      model_path)

                trim_missing_tc = report_missing_xpaths(full_report,
                                                        all_xpaths,
                                                        tc_xpaths,
                                                        excluded_xpaths,
                                                        is_submod)

                # Filter out all xpaths in the exclusion list
                trim_exception_tc = report_excluded_xpaths(full_report,
                                                           trim_missing_tc,
                                                           modelname,
                                                           excluded_xpaths)

                trim_broken_tc = report_broken_xpaths(full_report,
                                                      del_xpaths,
                                                      tc_xpaths)
                invalid_testcase = set()
                invalid_testcase, failed_test = report_invalid_testcases(full_report,
                                                                         obs_paths,
                                                                         tc_xpaths,
                                                                         tdl,
                                                                         excluded_xpaths)

                calculate_test_coverage(full_report,
                                        all_xpaths,
                                        tc_xpaths,
                                        trim_missing_tc,
                                        trim_exception_tc,
                                        excluded_xpaths,
                                        invalid_testcase,
                                        failed_tc)

                print_precommit_report_result(full_report,
                                              trim_missing_tc,
                                              no_cli,
                                              trim_broken_tc,
                                              no_cliver)

            if no_changes and not newmodel:
                return True
            if rem_item:
                for data in rem_item:
                    modelist.remove(data)

        else:
            fset = []
            fset.append(reportname)
            # TODO: copy models to tmpdir to filter out non-cedge model
            # Workaround is only for ned model
            test_model_subdir = get_model_subdir(reportname, modelpath)
            if "ned" in test_model_subdir:
                copy_ned_models(workspace, precommit_tmpdir)
                all_xpaths, obsolete_xpaths, is_submod = get_all_xpaths(
                        precommit_tmpdir,
                        modelpath,
                        fset)
                print(obsolete_xpaths)
            else:
                all_xpaths, obsolete_xpaths, is_submod = get_all_xpaths(
                        workspace,
                        modelpath,
                        fset)

            if not modelist:
                modelist.append((modelpath, fset[0]))
            for modelpath, modelname in modelist:
                tdl, error = get_test_data(os.path.join(workspace, model_test_path),
                                           modelpath,
                                           modelname,
                                           zipfile_path)
                if error:
                    # Unable to retrieve test data
                    return False

                tc_xpaths = get_test_xpaths(tdl)
                """
                if not reportname:
                    no_cli, no_cliver, no_operver, failed_tc = report_new_xpaths(
                            full_report,
                            new_xpaths,
                            mod_xpaths,
                            tdl)

                    report_deleted_xpaths(full_report, del_xpaths)
                """
                excluded_xpaths = get_excluded_xpaths(workspace,
                                                      model_test_path,
                                                      reportname,
                                                      excluded_xpath_filename,
                                                      modelpath)

                trim_missing_tc = report_missing_xpaths(full_report,
                                                        all_xpaths,
                                                        tc_xpaths,
                                                        excluded_xpaths,
                                                        is_submod)

                # Filter out all xpaths in the exclusion list
                trim_exception_tc = report_excluded_xpaths(full_report,
                                                           trim_missing_tc,
                                                           reportname,
                                                           excluded_xpaths)

                invalid_testcase = set()

                report_obsolete_xpaths(full_report,
                                       obsolete_xpaths)
                invalid_testcase, failed_tc = report_invalid_testcases(
                        full_report,
                        obsolete_xpaths,
                        tc_xpaths,
                        tdl,
                        excluded_xpaths)

                calculate_test_coverage(full_report,
                                        all_xpaths,
                                        tc_xpaths,
                                        trim_missing_tc,
                                        trim_exception_tc,
                                        excluded_xpaths,
                                        invalid_testcase,
                                        failed_tc)
            if bugid != 'none':
                add_cdets_enclosure(full_report,
                                    bugid, label,
                                    'yang-model-coverage')

    finally:
        save_log(full_report, logfile)
        shutil.rmtree(precommit_tmpdir)

    return True


def precommit_init():
    # Get Command Parameters
    parse = setup_args()
    args = parse.parse_args()

    return args


def main():
    """Entry Point for console script precommit.

       This is called by model coverage and precommit script.
       Model coverage script is for reporting coverage
       for a YANG model. Precommit script is for reporting
       coverage based off a model changeset.
    """
    # Get Command Parameters
    args = precommit_init()

    precommit_check(args.workspace, args.label, args.reportname,
                    args.bugid, args.report, args.logfile,
                    args.modelpath,  None)


if __name__ == '__main__':
    # Get Command Parameters
    main()
