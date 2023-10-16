# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
"""Analytics coverage APIs."""
import os
import shutil
import uuid
import json
import subprocess
from six import string_types

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from yangsuite import get_logger, get_path
from ysdevices.devprofile import YSDeviceProfile
from ysfilemanager import split_user_set, YSYangSet
from yscoverage.coverage import (
    YangCoverage,
    YangCoverageInProgress,
    YangCoverageException,
)
from yscoverage.dataset import ALL_COLUMNS, get_module_dataset
from yscoverage.get2edit import GetToEdit
from yscoverage.mibyang import MIBYANGpath
from yscoverage.mappings import (
    MibYangWriter,
    process_import_data,
    show_mapping_data,
    MappingException,
    merge_dictionaries,
    get_tree_dict
)


log = get_logger(__name__)


if not os.path.isfile(os.path.join(get_path('mibs_dir'), 'SNMPv2-MIB.my')):
    mib_path = get_path('mibs_dir')
    if os.path.isdir(mib_path):
        os.rmdir(mib_path)
    if os.path.isdir(os.path.join(os.path.dirname(__file__), 'mibs')):
        shutil.copytree(
            os.path.join(os.path.dirname(__file__), 'mibs'),
            mib_path
        )
    else:
        log.error('Cannot find MIB files')


@login_required
def render_main_page(request):
    """Return the main coverage.html page."""
    devices = YSDeviceProfile.list(require_feature="ssh")

    return render(request,
                  'yscoverage/coverage.html',
                  {'devices': devices})


@login_required
def getconfig(request):
    """Get running configuration from device."""
    device = request.POST.get('device')

    if not device:
        return JsonResponse({}, status=404, reason='No device')

    dev_profile = YSDeviceProfile.get(device)

    try:
        cfg = YangCoverage.get_config(dev_profile)
    except YangCoverageException as e:
        return JsonResponse({}, status=404, reason=str(e))

    return JsonResponse({'config': cfg})


def getreleases(request):
    """Get releases to choose from for model coverage."""
    if request.method == 'POST':
        ios = request.POST.get('ios')
        uri = request.POST.get(
            'uri',
            "http://yang-suite.cisco.com:8480/coverage/getreleases")

        if not ios:
            return JsonResponse({}, status=404, reason='No platform specified')

        releases = YangCoverage.get_releases(ios)

        if 'releases' in releases and not len(releases['releases']):
            # Try base server
            releases = YangCoverage.get_base_releases(uri + '?ios=' + ios)
            JsonResponse(releases)

        return JsonResponse(releases)
    else:
        ios = request.GET.get('ios', 'xe')

        releases = YangCoverage.get_releases(ios)

        return JsonResponse(releases)


@login_required
def getcoverage(request):
    """Get model coverage."""
    if request.method == 'POST':

        port = request.POST.get('port', '')
        cli = request.POST.get('cli')
        uri = request.POST.get('uri')
        timeout = request.POST.get('timeout', 120)
        convert_to_edit = request.POST.get('convert', 'true')
        edit_target = request.POST.get('target', 'running')
        coverage = ''
        xml = ''

        if not cli:
            return JsonResponse({}, status=404, reason='No config to test')

        while timeout:
            try:
                coverage, xml = YangCoverage.get_coverage(cli,
                                                          port,
                                                          uri)
                if convert_to_edit == 'true':
                    ge = GetToEdit(xml)
                    xml = ge.edit_config(edit_target)
                timeout = 0
            except YangCoverageInProgress:
                timeout -= 1
            except Exception as e:
                return JsonResponse({}, status=404, reason=str(e))

        result = {'coverage': coverage,
                  'xml': xml,
                  'average': YangCoverage.average_lines_per_second}

        return JsonResponse(result)

    else:

        return JsonResponse(YangCoverage.get_progress())


@login_required
def render_datasets_page(request):
    """Return the datasets.html page."""
    return render(request,
                  'yscoverage/dataset.html')


@login_required
def get_dataset(request):
    """Get XPath dataset for a given module and yangset."""
    if request.method == 'POST':
        models = request.POST.get('model')
        category = request.POST.get('category')
        yangset = request.POST.get('yangset')
        columns = request.POST.get('columns')
        fmt = request.POST.get('format')

        if not category or category == 'modules':
            if not models:
                return JsonResponse({}, status=400, reason='No model specified.')
            elif isinstance(models, string_types):
                models = json.loads(models)
                category = None
            else:
                return JsonResponse(
                    {}, status=400, reason='Invalid model specified.'
                )
        else:
            models = None

        if not yangset:
            return JsonResponse({}, status=400, reason='No yangset specified.')
        if not fmt:
            fmt = 'json'
        if not columns:
            columns = ALL_COLUMNS
        elif isinstance(columns, string_types):
            columns = json.loads(columns)

        owner, setname = split_user_set(yangset)

        ys_ds = get_module_dataset(
            fmt,
            owner=owner,
            base_set=setname,
            modules=models,
            columns=columns,
            category=category,
            add_support=True
        )

        if fmt == 'json':
            # Create the HTML using pandas.
            data = '<div class="container-fluid">'
            data += '<div class="row">'
            for i, mod in enumerate(models):
                if mod in ys_ds.dfs:
                    data += ys_ds.dfs[mod].to_html(
                        index_names=False,
                        justify='center'
                    )
                    data += '</div></div>'
                    if i + 1 != len(models):
                        data += '<div class="container-fluid">'
                        data += '<div class="row">'
            data += '</div></div>'
            return JsonResponse({'data': data})
        elif fmt == 'csv':
            if not os.path.isfile(ys_ds.csv_file):
                return JsonResponse({}, status=400, reason='Zipfile not found')

            with open(ys_ds.csv_file, 'rb') as zf:
                response = HttpResponse(zf, content_type='multipart/x-zip')
                response['Content-Disposition'] = \
                    'attachment; filename=dataset.zip'

                os.remove(ys_ds.csv_file)

                return response
        else:
            return JsonResponse({}, status=400, reason='Unrecognized "format"')
    else:
        return JsonResponse({}, status=400, reason='Invalid request method.')


@login_required
def get_diff(request):
    """Get diffs from two versions of model(s) or yangsets."""
    if request.method != 'POST':
        return JsonResponse({}, status=400, reason='Invalid request method.')
    category = request.POST.get('category')
    models = request.POST.get('model')
    compare_set = request.POST.get('compset')
    base_set = request.POST.get('baseset')
    columns = request.POST.get('columns')
    fmt = request.POST.get('format')

    if not category or category == 'modules':
        if not models:
            return JsonResponse({}, status=400, reason='No model specified.')
        elif isinstance(models, string_types):
            models = json.loads(models)
            category = None
        else:
            return JsonResponse(
                {}, status=400, reason='Invalid model specified.'
            )
    else:
        models = None

    if not columns:
        columns = ALL_COLUMNS
    elif isinstance(columns, string_types):
        columns = json.loads(columns)
    if not base_set:
        return JsonResponse({}, status=400, reason='No "from" yangset given.')
    if not compare_set:
        return JsonResponse({}, status=400, reason='No "to" yangset given.')
    if not fmt:
        fmt = 'json'

    try:
        owner, base_set = split_user_set(base_set)
        owner, compare_set = split_user_set(compare_set)

        base_ds = get_module_dataset(
            fmt, owner=owner, base_set=base_set, modules=models,
            columns=columns, compare_set=compare_set, category=category,
            add_support=True,
        )

        if fmt == 'json':
            # Create the HTML using pandas.
            data = '<div class="container-fluid"><div class="row">'
            for i, mod in enumerate(models):
                if mod not in base_ds.df_diffs:
                    data += '<p>' + mod + ' not proccessed.</p>'
                else:
                    diff = base_ds.df_diffs[mod]
                    if diff['diff'].empty:
                        data += '<h2>' + mod
                        data += ' matching xpaths have no differences</h2>'
                    else:
                        data += '<h2>Differences per Xpath: ' + mod + '</h2>'
                        data += diff['diff'].to_html(
                            index_names=False,
                            justify='center'
                        )
                    if diff['new'].empty:
                        data += '<h2>No new Xpaths</h2>'
                    else:
                        data += '<h2>New Xpaths</h2>'
                        data += diff['new'].to_html(
                            index_names=False,
                            justify='center'
                        )
                    if diff['removed'].empty:
                        data += '<h2>No Xpaths removed</h2>'
                    else:
                        data += '<h2>Removed Xpaths</h2>'
                        data += diff['removed'].to_html(
                            index_names=False,
                            justify='center'
                        )
                data += '</div></div>'
                if i + 1 != len(models):
                    data += '<div class="container-fluid"><div class="row">'
            data += '</div></div>'

            return JsonResponse({'data': data})

        if fmt == 'csv':
            if not os.path.isfile(base_ds.csv_file):
                return JsonResponse({}, status=400, reason='Zipfile not found')
            try:
                with open(base_ds.csv_file, 'rb') as zf:
                    response = HttpResponse(zf, content_type='multipart/x-zip')
                    response['Content-Disposition'] = \
                        'attachment; filename=diffset.zip'

                    os.remove(base_ds.csv_file)
                    return response
            except Exception as e:
                log.error(str(e))
                return JsonResponse({}, status=400, reason=str(e))
        else:
            return JsonResponse({}, status=400, reason='Unrecognized "format"')

    except Exception as e:
        log.error(str(e))
        return JsonResponse({'message': str(e)}, status=400, reason=str(e))


@login_required
def yang_snmp(request):
    devices = YSDeviceProfile.list(require_feature="netconf")

    return render(
        request,
        'yscoverage/yangsnmp.html',
        {'devices': devices}
    )


@login_required
def get_devices(request):
    devices = YSDeviceProfile.list(require_feature="netconf")
    return JsonResponse({'devices': devices})


@login_required
def get_yang_modules(request):
    owner = request.GET.get('owner')
    set_name = request.GET.get('setname')

    if set_name is not None:
        yang_set = YSYangSet.load(owner, set_name)
        modules = yang_set._modules
        return JsonResponse({'yangModules': modules})
    elif set_name is None:
        msg = 'Set name cannot be empty'
        return JsonResponse({}, status=500, reason=msg)


def _create_ui_list(mib_yang_path, oids_to_xpaths):
    """Convert dict to UI format with random IDs."""
    yang_paths = [{
        'label': 'No YANG XPath selected',
        'value': '',
        'id': 'no-xpath-selected'
    }]
    mib_paths = []
    mib_path_to_yang_path = {}
    tree = {}
    oid_to_numeric = mib_yang_path.translate_oids(
        dict.fromkeys(oids_to_xpaths.keys(), ''),
        to_numeric=True
    )

    # Create list of readable MIB paths, each list item has path and ID
    for oid, xpaths in oids_to_xpaths.items():
        mib_path = {
            # OID to identify Mapping in DB
            'oid': oid,
            'numeric': oid_to_numeric.get(
                oid,
                mib_yang_path.translate_oids([oid], to_numeric=True)[-1],
            ),
            # MIB path
            'value': oid,
            # Random ID to help frontend rendering
            'id': uuid.uuid4().__str__()
        }

        mib_paths.append(mib_path)
        xp_objs = []
        if xpaths:
            # Possible Xpath matches.
            for xpath in xpaths:
                xp_obj = {
                    'label': xpath,
                    'value': xpath,
                    'model': mib_yang_path.yobj.model,
                    'id': uuid.uuid4().__str__()
                }
                xp_objs.append(xp_obj)
            mib_path_to_yang_path[oid] = xp_objs
        else:
            mib_path_to_yang_path[oid] = []

        # Do not render N/A OIDs
        if 'n/a' not in oid.lower():
            curr_tree = get_tree_dict(oid)
            if tree:
                # Merge this tree to the main tree
                tree = merge_dictionaries(tree, curr_tree)
            else:
                # No tree exists yet, create it
                tree = curr_tree
    # Create list of YANG XPaths, each list item has YANG XPath and ID
    for xpath in mib_yang_path.yobj.xpaths:
        yang_paths.append({
            'value': xpath,
            'label': xpath,
            'model': mib_yang_path.yobj.model,
            # Random ID to help frontend rendering
            'id': uuid.uuid4().__str__()
        })
    return (yang_paths, mib_paths, mib_path_to_yang_path, tree)


@login_required
def match_oids_to_xpaths(request):
    """Try to match list of OIDs to list of Xpaths."""
    user_obj = request.user
    user = user_obj.username
    yang_module = request.GET.get('yangmodule')
    yang_module_revision = request.GET.get('yangmodulerevision')
    yang_set = request.GET.get('setname')
    device_name = request.GET.get('device')
    force_walk = request.GET.get('forcewalk')
    community = request.GET.get('community', '')
    v3pwd = request.GET.get('v3password', '')
    map_filename = request.GET.get('mapfile', '')
    starting_oids = request.GET.get('oids', '')

    if not device_name:
        return JsonResponse(
            {},
            status=400,
            reason="Must select a device."
        )
    if not community and not v3pwd:
        return JsonResponse(
            {},
            status=400,
            reason="Please input community string or SNMPv3 password."
        )

    device_profile = YSDeviceProfile.get(device_name)
    if not hasattr(device_profile, 'netconf'):
        # Device must support NETCONF
        return JsonResponse(
            {},
            status=500,
            reason='Device is not configured for NETCONF'
        )
    if community:
        # SNMP community string used
        device_profile.base.username = community
        device_profile.base.password = ''
    elif v3pwd:
        # SNMPv3 password used
        device_profile.base.password = v3pwd
    else:
        return JsonResponse(
            {},
            status=403,
            reason='Need SNMPv3 password or community string.'
        )

    try:
        # Dynamically map OIDs to XPaths using device's values
        mib_yang_path = MIBYANGpath.get(
            yang_module,
            user,
            device_profile,
            yangset=yang_set,
            map_filename=map_filename,
            starting_oids=starting_oids,
            model_revision=yang_module_revision
        )
        if force_walk.lower() == 'true':
            # remove all SNMP walk data to force a new SNMP walk
            mib_yang_path.force_walk(yang_module, user)

        oids_to_xpaths = mib_yang_path.get_device_oids_to_xpaths_map()

        (xpaths, mib_paths, mib_path_to_xpath, tree_data) = _create_ui_list(
            mib_yang_path,
            oids_to_xpaths,
        )
        return JsonResponse({
            'yangPaths': xpaths,
            'mibPaths': mib_paths,
            'mibPathToYangPath': mib_path_to_xpath,
            'modelsToYangPath': mib_yang_path.modules_to_matched_xpaths,
            'treeData': tree_data
        })
    except Exception as exc:
        return JsonResponse(
            {'message': str(exc)},
            status=500,
            reason=str(exc)
        )


@login_required
def save_mapping(request):
    """Save OIDs and Xpaths in XLSX spreadsheet."""
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'selectedYangPath' not in body:
        return JsonResponse(
            {'message': 'No XPath found.'},
            status=400,
            reason='No XPath found.'
        )

    oid = body['oid']
    yang_module = body['yangModule']
    yang_paths = body['yangPaths']
    mib_paths = body['mibPaths']
    mib_to_yang_paths = body['mibPathToYangPath']
    mapfile = body['mapFile']

    if 'modelsToYangPath' in body:
        model_to_xpath = body['modelsToYangPath']
    else:
        model_to_xpath = {}

    try:
        mypath = MIBYANGpath.get(yang_module, request.user.username)
        if not mapfile:
            if not yang_module:
                return JsonResponse(
                    {'message': 'Choose model (needed to "Save" mapping).'},
                    status=400,
                    reason='Choose model (needed to "Save" mapping).'
                )
            if not mypath:
                return JsonResponse(
                    {'message': 'Execute "Match OIDs to Xpaths" again.'},
                    status=500,
                    reason='"Match OIDs to Xpaths" must be executed again.'
                )
            mapfile = os.path.basename(
                mypath.walk_file
            ).replace('.walk', '.csv')
        map_file = os.path.join(
            get_path('mibyang_mappings_dir', user=request.user.username),
            mapfile
        )

        myw = MibYangWriter.get(
            map_file,
            request.user.username,
            mib_paths,
            yang_paths,
            model_to_xpath,
            yang_module,
        )
        myw.save_mapping_in_csv(
            oid=oid,
            mib_to_yang_paths=mib_to_yang_paths,
            mibyang_path=mypath
        )
    except Exception as e:
        log.error(str(e))
        return JsonResponse(
            {'message': str(e)},
            status=500,
            reason=str(e)
        )
    return JsonResponse({}, status=204)


@login_required
def delete_mapping(request):
    oid = request.GET.get('oid')
    yang_module = request.GET.get('yangmodule')
    mapfile = request.GET.get('mapFile')

    try:
        if not mapfile:
            if not yang_module:
                return JsonResponse(
                    {'message': 'Choose model (needed to "Delete" mapping).'},
                    status=400,
                    reason='Choose model (needed to "Delete" mapping).'
                )
            mypath = MIBYANGpath.get(
                yang_module,
                request.user.username
            )
            mapfile = os.path.basename(
                mypath.walk_file
            ).replace('.walk', '.csv')
        map_file = os.path.join(
            get_path('mibyang_mappings_dir', user=request.user.username),
            mapfile,
        )
        myw = MibYangWriter.get(
            map_file,
            request.user.username,
        )
        myw.delete_mapping_in_csv(oid)
    except Exception as e:
        if hasattr(e, 'msg'):
            log.error(e.msg)
            return JsonResponse(
                {'message': e.msg},
                status=500,
                reason=e.msg
            )
        else:
            log.error(str(e))
            return JsonResponse(
                {'message': str(e)},
                status=500,
                reason=str(e)
            )

    return JsonResponse({}, status=204)


@login_required
def import_mappings(request):
    """Import spreadsheet data from UI and present back to UI."""
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    file_data = body.get('fileDataArray')  # Contents of files

    if file_data is None:
        return JsonResponse(
            {'message': 'No data in spreadsheet.'},
            status=400,
            reason='No data in spreadsheet.'
        )
    if isinstance(file_data, list) and len(file_data) == 1:
        filename = file_data[0].get('filename')
        filename = filename.replace('.xlsx', '.csv')
        file_path = os.path.join(
            get_path('mibyang_mappings_dir', user=request.user.username),
            filename
        )
    else:
        return JsonResponse(
            {'message': 'Unrecognized spreadsheet data.'},
            status=400,
            reason='Unrecognized spreadsheet data.'
        )
    data = process_import_data(file_data, file_path, request.user.username)
    # TODO: the data is all empty because show mappings handles it now.
    mib_paths, yang_paths, mib_path_to_yang_path = data

    return JsonResponse({
        'yangPaths': yang_paths,
        'mibPaths': mib_paths,
        'mibPathToYangPath': mib_path_to_yang_path
    })


@login_required
def get_oid_result(request):
    """Send single OID to device and return result."""
    # TODO: Merge this code with get_device_oids_to_values in MIBYANGpath
    oid = request.GET.get('oid', '')
    device_name = request.GET.get('device', '')
    community = request.GET.get('community', '')
    v3pwd = request.GET.get('v3password', '')

    if not device_name:
        return JsonResponse(
            {},
            status=400,
            reason="Must select a device."
        )
    if not community and not v3pwd:
        return JsonResponse(
            {},
            status=400,
            reason="Please input community string or SNMPv3 password."
        )

    device_profile = YSDeviceProfile()
    device = device_profile.get(device_name)
    device_username = device.dict()['base']['username']
    device_address = device.dict()['base']['address']

    if v3pwd:
        cmd = [
            'snmpwalk',
            '-v3',
            '-l',
            'authNoPriv',
            '-Of',
            '-Pu',
            '-M', get_path('mibs_dir'),
            '-m', 'ALL',
            '-u',
            device_username,
            '-a',
            'MD5',
            '-A',
            v3pwd,
            device_address
        ]
    else:
        cmd = [
            'snmpwalk',
            '-Of',
            '-Pu',
            '-M', get_path('mibs_dir'),
            '-m', 'ALL',
            '-v2c',
            '-c',
            community,
            device_address,
            oid
        ]
    log.info(f'Running SNMP cmd: {" ".join(cmd)}')
    # Run the command
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    result, _ = process.communicate()
    if result:
        result = result.strip()
    else:
        result = 'OID does not exist or device is unreachable.'
    return JsonResponse({'result': result})


@login_required
def get_map_result(request):
    """Get OID result and Xpath result and compare."""
    body = json.loads(request.body.decode('utf-8'))
    model = body.get('model')
    yangset = body.get('yangset')
    oid = body.get('oid', '')
    xpath = body.get('xpath', '')
    device = body.get('device')
    community = body.get('community', '')
    v3pwd = body.get('v3password', '')

    if not device:
        return JsonResponse(
            {'message': "Choose device."},
            status=400,
            reason="Choose device."
        )
    if not community and not v3pwd:
        return JsonResponse(
            {},
            status=400,
            reason="Please input community string or SNMPv3 password."
        )
    if not model:
        return JsonResponse(
            {'message': 'Choose model (need namespace for "Run").'},
            status=400,
            reason='Choose model (need namespace for "run").'
        )

    if not xpath:
        return JsonResponse(
            {'message': "No YANG XPath."},
            status=400,
            reason="No YANG XPaths."
        )
    if not oid:
        return JsonResponse(
            {'message': "No OID."},
            status=400,
            reason="No OID."
        )

    try:
        dev_profile = YSDeviceProfile.get(device)
        if community:
            # SNMP community string used
            dev_profile.base.username = community
            dev_profile.base.password = ''
        elif v3pwd:
            # SNMPv3 password used
            dev_profile.base.password = v3pwd
        mypath = MIBYANGpath.get(
            model, request.user.username, dev_profile, yangset
        )
        if model != mypath.yobj.model:
            mypath.yobj.model = model
        result = mypath.run_compare(oid, xpath)
    except Exception as exc:
        return JsonResponse(
            {'message': str(exc)},
            status=500,
            reason=str(exc)
        )

    return JsonResponse(result)


@login_required
def get_mapping_filenames(request):
    """Return a list of all XLSX filenames with mappings."""
    mappings_dir = get_path('mibyang_mappings_dir', user=request.user.username)
    mapping_filenames = [{
        'label': 'No mapping file selected',
        'value': '',
        'id': 'none'
    }]

    for (dpath, dnames, fnames) in os.walk(mappings_dir):
        for fname in fnames:
            if fname.startswith('~'):
                # Excel saves copies when file is open in Excel so skip it.
                continue
            if '.csv' in fname:
                mapping_filenames.append(
                    {
                        'id': uuid.uuid4().__str__(),
                        'value': fname,
                        'label': fname
                    }
                )
        # Break after all the files in top-most directory have been scanned
        break
    return JsonResponse({
        'mappingFilenames': mapping_filenames
    })


@login_required
def import_show_mappings_file(request):
    """Show mapping data from imported or newly mapped spreadsheets."""
    filename = request.GET.get('filename', '')
    filepath = os.path.join(
        get_path('mibyang_mappings_dir', user=request.user.username),
        filename
    )

    try:
        mib_paths, yang_paths, mpath_to_ypath, model_xp, tree = show_mapping_data(
            filepath, request.user.username, MIBYANGpath.translate_oids
        )
    except (MappingException, Exception) as exc:
        return JsonResponse(
            {'message': str(exc)},
            status=500,
            reason=str(exc)
        )

    return JsonResponse({
        'mibPaths': mib_paths,
        'yangPaths': yang_paths,
        'mibPathToYangPath': mpath_to_ypath,
        'modelsToYangPath': model_xp,
        'treeData': tree,
    })


@login_required
def export_mapping_file(request):
    """Export mapping data spreadsheet."""
    filepath = request.GET.get('filepath', '')
    filepath = os.path.join(
        get_path('mibyang_mappings_dir', user=request.user.username),
        filepath
    )

    if not os.path.isfile(filepath):
        return JsonResponse(
            {'message': f'{filepath} not found.'},
            status=500,
            reason=f'{filepath} not found.'
        )

    try:
        filedata = open(filepath).read()
        return JsonResponse(
            {'filedata': filedata},
            status=200,
        )
    except Exception as exc:
        return JsonResponse(
            {'message': str(exc)},
            status=500,
            reason=str(exc),
        )


@login_required
def find_mappings(request):
    user = request.user.username
    body = json.loads(request.body.decode('utf-8'))
    # Translate OIDs, only search with human-readable OIDs
    oids = MIBYANGpath.translate_oids(body.get('oids', []))
    # Filenames mapped to the mappings found in that file
    result = {'rows': [], 'columns': []}

    try:
        # Get all imported/saved mapping filenames and find OIDs from there
        mappings_path = get_path('mibyang_mappings_dir', user=request.user.username)
        for (_, _, fnames) in os.walk(mappings_path):
            for fname in fnames:
                if fname.endswith('.csv'):
                    filepath = os.path.join(mappings_path, fname)
                    writer = MibYangWriter.get(filepath, user)
                    rows, columns = writer.find_mappings(
                        oids,
                        filepath,
                        fname,
                        MIBYANGpath.translate_oids,
                        MIBYANGpath.label_oid_keys,
                    )
                    if rows:
                        result['rows'] += rows
                    if columns:
                        result['columns'] = columns
            break
    except Exception as exc:
        return JsonResponse(
            {'message': str(exc)},
            status=500,
            reason=str(exc),
        )

    return JsonResponse({'result': result}, status=200)
