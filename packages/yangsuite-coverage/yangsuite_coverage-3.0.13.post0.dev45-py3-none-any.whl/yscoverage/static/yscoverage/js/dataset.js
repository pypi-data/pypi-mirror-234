/**
 * Module for YANG datasets.
 */
let dataset = function() {
    /**
     * Default configuration of this module.
     */
    let config = {
        /* Selector string for a progressbar */
        progress: 'div#ys-progress',
        getdataseturi: "/coverage/getdataset/",
        datasetdiffuri: "/coverage/getdiff/",
        diffinfouri: "/coverage/diffinfo/",
        datasetinfouri: "/coverage/datasetinfo/",

        baseYangSet: "select#ys-primary-yangset",
        compareYangset: "select#ys-secondary-yangset",
        yangModules: "select#ys-module",
        yangModuleOptions: "select#ys-module option",
        dependencies: "select#ys-include-dependencies",
        columns: "select#ys-columns",
        columnsExcluded: "select#ys-columns-excluded",
        modalDialog: "div#modalDiv",
        // TODO: columnList should come from backend.
        columnList: [
            'xpath',
            'nodetype',
            'module',
            'datatype',
            'basetype',
            'leafref_path',
            'when',
            'must',
            'deviation',
            'mandatory',
            'patterns',
            'name',
            'description',
            'revision',
            'xpath_pfx',
            'base',
            'prefix',
            'namespace',
            'schema_node_id',
            'access',
            'operations',
            'key',
            'presence',
            'default',
            'options',
            'presence',
            'min',
            'max',
            'typespec',
            'units',
            'members',
            'fraction_digits',
            'minLength',
            'maxLength'
        ]
    };

    let c = config;     // internal alias for brevity

    let dsWin = null;  // WindowProxy for displaying results.

    /*
     * getDatasetInfo opens a websocket to handle updates from the backend.
     * It is possible for the backend to try to send events before websocket
     * connects so need backend callback onopen.
     *
     * @param {string} type - 'dataset' or 'diff'
     * @param {function} callback - function to call when websocket is open
     * @param {string[]} models - list of models to get dataset for
     * @param {string} category - category to get dataset for
     * @returns {WebSocket} - websocket object
     */
    function getDatasetInfo(type, callback, models, category=null) {
        let done = false;
        ws = new WebSocket("ws://" + window.location.host + "/ws/coverage/datasetinfo/");
        ws.onmessage = function(e) {
            let data = JSON.parse(e.data);
            if (type == 'diff' && data.progress == "done") {
                done = true;
            } else if (type == 'dataset' && data.progress == "Datasets done") {
                done = true;
            }
            if (done) {
                ws.close();
                return;
            }
            try {
                setProgressText($(c.progress), data.progress);
            } catch (e) {
                ws.close();
            }
        }
        ws.onopen = function(e) {
            startProgress($(c.progress));
            // TODO: what if this fails?
            callback(models, category, ws);
        }
        ws.onclose = function(e) {
            stopProgress($(c.progress));
        }
        return ws;
    }

    function getColumnList() {
        return c.columnList;
    }

    /*
     * resolveColumnList returns a list of columns to include in the dataset
     * based on Excluded and Included lists.  If columns is empty, it returns
     * the default column list.
     *
     * @returns {string[]} - list of columns to include
     */
    function resolveColumnList() {
        let columns = $(c.columns).val();
        let removeColumns = $(c.columnsExcluded).val();

        if (!columns) {
            columns = new Set(getColumnList());
        } else {
            columns = new Set(columns);
        }

        if (removeColumns) {
            for (let col of removeColumns) {
                columns.delete(col);
            }
        }
        return Array.from(columns);
    }

    /*
     * checkModel checks if the model is empty or if there are multiple models.
     * If multiple models, it displays a warning and asks the user to confirm
     * that they want to continue with the display.  If the models are big,
     * the display will be overwhelming.  In that case it would be better to
     * download the dataset and view it in a spreadsheet.
     *
     * @param {string[]} model - list of models to check
     * @param {string} text - text to display in warning
     * @param {function} callback - function to call if user confirms
     * @returns {function} - callback function
     */
    function checkModel(model, callback, category=null, type='dataset', action='display') {
        if (!$("#ys-primary-yangset").val()) {
            alert("Please select YANG set(s)");
            return;
        }
        if (!model && !category) {
            alert("Please select a module or category");
            return;
        }
        let warnDiff = false;
        // Alternative message if display is chosen.
        let warnText = 'Download dataset';

        if (type == 'diff') {
            // Check if "revision" is excluded from columns.
            let excludes = $(c.columnsExcluded).val();
            if (!excludes || !excludes.includes('revision')) {
                warnDiff = true;
            }
        }
        if (action == 'download') {
            if (!warnDiff) {
                // Number of modules does not matter and revision is not excluded.
                getDatasetInfo(type, callback, model, category);
                return;
            }
        } else {
            if (type == 'diff') {
                // Alternative message if display is chosen.
                warnText = 'Download dataset differences';
            }
        }

        if ((model && model.length > 1) || warnDiff) {
            $(c.modalDialog).empty();
            $(c.modalDialog).dialog({
                modal: true,
                height: "auto",
                width: "auto",
                open: function( e, ui ) {
                    $( this ).siblings( ".ui-dialog-titlebar" )
                            .find( "button" ).blur();
                },
                buttons: [
                    {
                        text: "Continue",
                        click: function() {
                            $(this).dialog("close");
                            getDatasetInfo(type, callback, model, category);
                        }
                    },
                    {
                        text: "Cancel",
                        click: function() {
                            stopProgress($(c.progress));
                            $(this).dialog("close");
                            return;
                        }
                    }
                ]
            });
            let htmlMsg = "";
            if (model && model.length > 1) {
                htmlMsg = '<p><strong>WARNING: </strong> '+
                '<p>Displaying more than one model may result in the page not '+
                'loading.  Use "' + warnText + '" instead.</p>';
            }
            if (warnDiff) {
                htmlMsg += '<p><strong>WARNING: </strong> '+
                '<p>You may want "revision" excluded from diffs, '+
                'otherwise all nodes will show a change in revision.</p>'+
                '<p>Click on Cancel and add revision to excluded columns or Continue.</p>';
            }
            $(c.modalDialog).html(htmlMsg);
            $(c.modalDialog).dialog("open");
        } else {
            getDatasetInfo(type, callback, model, category);
        }
    }

    /*
     * getDataset starts processing of a dataset.  User selects one or more
     * models and then clicks the "Submit" button.  This function
     * validates the input, starts the websocket to handle status updates,
     * and then calls getDatasetContinue to start the processing.
     *
     * @param {string[]} models - list of models to get dataset for
     */
    function getDataset(models) {
        checkModel(models, getDatasetContinue, category=null, type='dataset', action='display');
    }

    /*
     * getDatasetContinue starts processing of a dataset after the user has
     * confirmed that they want to continue and the status websocket is open.
     * It opens a new window and displays the results in a table format.
     *
     * @param {string[]} models - list of models to get dataset for
     */
    function getDatasetContinue(model) {
        let yangset = $(c.baseYangSet).val();
        let columns = resolveColumnList();

        if (dsWin) {
            dsWin.close();
            dsWin = null;
        }

        getPromise(c.getdataseturi, {
            yangset: yangset,
            model: JSON.stringify(model),
            columns: JSON.stringify(columns),
            format: 'json',
        }).then(function(retObj) {
            let title = "";
            for (let i=0; i<model.length; i++) {
                title += model[i]
                if (i + 1 != model.length) {
                    title += " - ";
                }
            }
            dsWin = window.open(
                '',
                title,
                "height=auto overflow=auto width=1271px, scrollbars=yes"
            );
            dsWin.document.write("<title>" + title + "</title>");
            dsWin.document.write(retObj.data);
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
        });
    }

    /*
     * downloadDataset starts processing of a dataset download.  User selects one or
     * more models and then clicks the "Submit" button.  This function starts a
     * websocket to handle status updates and then calls downloadDatasetContinue.
     *
     * @param {string[]} models - list of models to get dataset for
     * @param {string} category - category to get dataset for
     */
    function downloadDataset(models, category) {
        checkModel(models, downloadDatasetContinue, category, type='dataset', action='download');
    }

    /*
     * downloadDatasetContinue starts processing of a dataset download after the
     * status websocket is open.  A .csv spreadsheet is downloaded.
     *
     * @param {string[]} models - list of models to get dataset for
     * @param {string} category - category to get dataset for
     * @param {WebSocket} ws - websocket object
     */
    function downloadDatasetContinue(models, category=null, ws=null) {
        let yangset = $(c.baseYangSet).val();
        let columns = resolveColumnList();

        if (models) {
            models = JSON.stringify(models);
        }

        $.ajax({
            url: c.getdataseturi,
            method: 'POST',
            data: {
                format: 'csv',
                yangset: yangset,
                category: category,
                model: models,
                columns: JSON.stringify(columns),
            },
            xhrFields: {
                responseType: 'blob',
                onload: function (data) {
                    if (this.status != 200) {
                        popDialog("Error " + this.status + ": " + this.statusText);
                        return;
                    }
                    let a = document.createElement('a');
                    let url = window.URL.createObjectURL(data.target.response);
                    a.href = url;
                    a.download = 'dataset.zip';
                    document.body.append(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                },
                onclose: function() {
                    if (ws) {
                        ws.close();
                    } else {
                        stopProgress($(c.progress));
                    }
                }
            }
        });
    }

    /*
     * getDatasetDiff starts processing of a dataset diff.  User selects one or
     * more models and then clicks the "Submit" button.  This function validates
     * the input, starts the websocket to handle status updates, and then calls
     * getDatasetDiffContinue to start the processing.
     *
     * @param {string[]} models - list of models to get dataset for
     */
    function getDatasetDiff(models) {
        checkModel(models, getDatasetDiffContinue, category=null, type='diff', action='display');
    }

    /*
     * getDatasetDiffContinue starts processing of a dataset diff after the user
     * has confirmed that they want to continue and the status websocket is open.
     * It opens a new window and displays the results in a table format.
     *
     * @param {string[]} models - list of models to get dataset for
     * @param {WebSocket} ws - websocket object
     */
    function getDatasetDiffContinue(model, ws=null) {
        let compset = $(c.baseYangSet).val();
        let baseset = $(c.compareYangset).val();
        let columns = resolveColumnList();

        if (!compset || !baseset) {
            alert("Please select Base YANG set and Compare YANG set.");
            stopProgress(progressBar);
            return;
        }

        if (dsWin) {
            dsWin.close();
            dsWin = null;
        }
        getPromise(c.datasetdiffuri, {
            model: JSON.stringify(model),
            compset: compset,
            baseset: baseset,
            columns: JSON.stringify(columns),
            format: 'json',
        }).then(function(retObj) {
            let title = baseset.split("+")[1] + " - " + compset.split("+")[1] + ": ";
            for (let i=0; i<model.length; i++) {
                title += model[i]
                if (i + 1 != model.length) {
                    title += ", ";
                }
            }
            dsWin = window.open(
                '',
                title,
                "height=auto overflow=auto width=1271px, scrollbars=yes"
            );
            dsWin.document.write("<title>" + title + "</title>");
            dsWin.document.write(retObj.data);
            if (ws) {
                ws.close();
            } else {
                stopProgress($(c.progress));
            }
        }, function(retObj) {
            popDialog("Error " + retObj.status + ": " + retObj.statusText);
            if (ws) {
                ws.close();
            } else {
                stopProgress($(c.progress));
            }
        });
    }

    /*
     * downloadDatasetDiff starts processing of a dataset diff download.  User
     * selects one or more models and then clicks the "Submit" button.  This
     * function starts a websocket to handle status updates and then calls
     * downloadDatasetDiffContinue.
     *
     * @param {string[]} models - list of models to get dataset for
     * @param {string} category - category to get dataset for
     */
    function downloadDatasetDiff(models, category) {
        checkModel(models, downloadDatasetDiffContinue, category, type='diff', action='download');
    }

    /*
     * downloadDatasetDiffContinue starts processing of a dataset diff download
     * after the status websocket is open.  A .csv spreadsheet is downloaded.
     *
     * @param {string[]} models - list of models to get dataset for
     * @param {string} category - category to get dataset for
     * @param {WebSocket} ws - websocket object
     */
    function downloadDatasetDiffContinue(models, category, ws=null) {
        let compset = $(c.compareYangset).val();
        let baseset = $(c.baseYangSet).val();
        let columns = resolveColumnList();

        if (models) {
            models = JSON.stringify(models);
        }

        $.ajax({
            url: c.datasetdiffuri,
            method: 'POST',
            data: {
                format: 'csv',
                compset: compset,
                baseset: baseset,
                category: category,
                model: models,
                columns: JSON.stringify(columns),
            },
            xhrFields: {
                responseType: 'blob',
                onload: function (data) {
                    if (this.status != 200) {
                        popDialog("Error " + this.status + ": " + this.statusText);
                        if (ws) {
                            ws.close();
                        }
                        return;
                    }
                    let a = document.createElement('a');
                    let url = window.URL.createObjectURL(data.target.response);
                    a.href = url;
                    a.download = 'diffset.zip';
                    document.body.append(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    if (ws) {
                        ws.close();
                    }
                }
            }
        });
    }

    /**
     * Public API.
     */
    return {
        config: config,
        getDataset: getDataset,
        downloadDataset: downloadDataset,
        getDatasetDiff: getDatasetDiff,
        downloadDatasetDiff: downloadDatasetDiff,
        getColumnList: getColumnList,
    };
}();