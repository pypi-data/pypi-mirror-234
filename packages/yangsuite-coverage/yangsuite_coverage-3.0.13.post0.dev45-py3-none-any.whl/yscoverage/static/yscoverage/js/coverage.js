/**
 * Module for YANG coverage.
 */
let coverage = function() {
    /**
     * Default configuration of this module.
     */
    let config = {
        /* Selector string for a progressbar */
        progress: 'div#ys-progress',
        clitextarea: "textarea#ycov-cli",
        xmltextarea: "textarea#ycov-xml",
        resultdiv: "div#ycov-results",
        modsdiv: "div#ycov-models",
        downloadbtn: "button#ycov-coverage-download",
        clearresultbtn: "button#ycov-clear-result",
        clearcfg: "button#ycov-clear-cfg",
        getconfiguri: "/coverage/getconfig/",
        getreleaseuri: "/coverage/getreleases/",
        getcoverageuri: "/coverage/getcoverage/",
        releases: "select#ycov-releases",
    };

    let c = config;     // internal alias for brevity

    let local = {
        downloadResult: "",
    }

    function getConfig(device) {
        startProgress($(c.progress));

        $.when(getPromise(c.getconfiguri, {device: device}))
        .then(function(retObj) {
            $(c.clitextarea).val(retObj.config);
            stopProgress($(c.progress));
            $(c.clearcfg).show();
        })
        .fail(function(retObj) {
            stopProgress($(c.progress));
            popDialog("<pre>Status: " + retObj.status + " " + retObj.statusText + "</pre>");
        });
    }

    function getReleases(ios='xe') {
        $.when(getPromise(c.getreleaseuri, {'ios': ios}))
        .then(function(retObj) {
            for (let rel of retObj.releases) {
                $(c.releases).append(
                    '<option value="' + rel.port + '">' + rel.name + '</option>');
            }
        })
        .fail(function(retObj) {
            popDialog("<pre>Status: " + retObj.status + " " + retObj.statusText + "</pre>");
        });
    }

    /**
     *
     * @param {string} port
     * @param {string} fmt One of "graphical", "plaintext"
     */
    function getCoverage(port) {
        config = $(c.clitextarea).val()
        startProgress($(c.progress), c.getcoverageuri);
        $(c.modsdiv).empty();
        $(c.resultdiv).empty();
        let plaintextContent = "";

        local.downloadResult = "";

        $.when(getPromise(c.getcoverageuri, {'port': port,
                                             'cli': config}))
        .then(function(retObj) {
            let cli = "";
            let mods = new Set();

            $(c.resultdiv).append('<p><strong>Missing coverage highlighted in red:</strong></p>');
            for (let line of retObj.coverage.split('\n')) {
                if (line.startsWith('!&')) {
                    line = line.replace('!&', '  ');
                    cli += '<strong style="color: red;">' + line + '</strong>\n';
                } else {
                    cli += line + '\n';
                }
            }
            $(c.resultdiv).append('<pre>' + cli + '</pre>');

            plaintextContent += "====================================\n";
            plaintextContent += "Configuration CLI\n";
            plaintextContent += 'Missing coverage is marked with "!&"\n';
            plaintextContent += "====================================\n";
            plaintextContent += retObj.coverage;

            for (let line of retObj.xml.split('\n')) {
                if (line.indexOf('xmlns') > -1 && line.indexOf('netconf:base') == -1) {
                    if (line.indexOf('">') > -1) {
                        mods.add(line.slice(line.indexOf('xmlns="') + 7, line.indexOf('">')));
                    } else if (line.indexOf('"/>') > -1) {
                        mods.add(line.slice(line.indexOf('xmlns="') + 7, line.indexOf('"/>')));
                    }
                }
            }
            if (mods.size > 0) {
                let models = "";

                $(c.modsdiv).append('<p><strong>Models used in config:</strong></p>');
                mods.forEach(function(mod) {
                    models += mod + "\n";
                });
                $(c.modsdiv).append('<pre>' + models + '</pre>');

                plaintextContent += "\n====================================\n";
                plaintextContent += "Models used in configuration\n";
                plaintextContent += "====================================\n";
                mods.forEach(function(mod) {
                    plaintextContent += mod + "\n";
                });
            }

            let rows = retObj.xml.split('\n').length;
            if (rows > 25) {
                $(c.xmltextarea).attr("rows", rows);
            } else {
                $(c.xmltextarea).attr("rows", 25);
            }
            $(c.xmltextarea).val(retObj.xml);

            plaintextContent += "\n====================================\n";
            plaintextContent += "Configuration XML\n";
            plaintextContent += "====================================\n";
            plaintextContent += retObj.xml;

            local.downloadResult = plaintextContent;
            $(c.downloadbtn).show();
            $(c.clearresultbtn).show();

            stopProgress($(c.progress));
        })
        .fail(function(retObj) {
            stopProgress($(c.progress));
            popDialog("<pre>Status: " + retObj.status + " " + retObj.statusText + "</pre>");
        });
    }

    function downloadResult() {
        if (local.downloadResult.length == 0) {
            return;
        }
        let element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' +
                             encodeURIComponent(local.downloadResult));
        element.setAttribute('download', 'coverage.txt');
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }

    /**
     * Public API.
     */
    return {
        config: config,
        getConfig: getConfig,
        getReleases: getReleases,
        getCoverage: getCoverage,
        downloadResult: downloadResult,
    };
}();