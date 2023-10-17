"use strict";
(self["webpackChunkjupyterlab_sql_editor"] = self["webpackChunkjupyterlab_sql_editor"] || []).push([["lib_index_js"],{

/***/ "./lib/constants.js":
/*!**************************!*\
  !*** ./lib/constants.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Constants: () => (/* binding */ Constants)
/* harmony export */ });
var Constants;
(function (Constants) {
    Constants.SHORT_PLUGIN_NAME = 'jupyterlab-sql-editor';
    Constants.FORMAT_COMMAND = `${Constants.SHORT_PLUGIN_NAME}:format_cell`;
    Constants.FORMAT_COMMAND_DOCUMENT = `${Constants.SHORT_PLUGIN_NAME}:format_document`;
    Constants.LONG_PLUGIN_NAME = `${Constants.SHORT_PLUGIN_NAME}`;
    Constants.SETTINGS_SECTION = `${Constants.LONG_PLUGIN_NAME}:plugin`;
})(Constants || (Constants = {}));


/***/ }),

/***/ "./lib/formatter.js":
/*!**************************!*\
  !*** ./lib/formatter.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   JupyterLabCodeFormatter: () => (/* binding */ JupyterLabCodeFormatter),
/* harmony export */   SqlFormatter: () => (/* binding */ SqlFormatter)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var sql_formatter__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! sql-formatter */ "webpack/sharing/consume/default/sql-formatter/sql-formatter");
/* harmony import */ var sql_formatter__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(sql_formatter__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./constants */ "./lib/constants.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");




class SqlFormatter {
    constructor(formatTabWidth, formatUseTabs, formatKeywordCase) {
        this.formatTabWidth = formatTabWidth;
        this.formatUseTabs = formatUseTabs;
        this.formatKeywordCase = formatKeywordCase;
    }
    format(text) {
        const formatted = (0,sql_formatter__WEBPACK_IMPORTED_MODULE_1__.format)(text || '', {
            language: 'spark',
            tabWidth: this.formatTabWidth,
            useTabs: this.formatUseTabs,
            keywordCase: this.formatKeywordCase,
            linesBetweenQueries: 2 // Defaults to 1
        });
        return formatted;
    }
}
class JupyterlabNotebookCodeFormatter {
    constructor(notebookTracker, codeMirror, sqlFormatter) {
        this.working = false;
        this.notebookTracker = notebookTracker;
        this.extractors = [];
        this.extractors.push((0,_utils__WEBPACK_IMPORTED_MODULE_2__.cellMagicExtractor)('sparksql'));
        this.extractors.push((0,_utils__WEBPACK_IMPORTED_MODULE_2__.cellMagicExtractor)('trino'));
        this.extractors.push((0,_utils__WEBPACK_IMPORTED_MODULE_2__.markerExtractor)('sparksql'));
        this.extractors.push((0,_utils__WEBPACK_IMPORTED_MODULE_2__.markerExtractor)('trino'));
        this.codeMirror = codeMirror;
        this.sqlFormatter = sqlFormatter;
    }
    setFormatter(sqlFormatter) {
        this.sqlFormatter = sqlFormatter;
    }
    async formatAction() {
        return this.formatCells(true);
    }
    async formatSelectedCodeCells(notebook) {
        return this.formatCells(true, notebook);
    }
    getCodeCells(selectedOnly = true, notebook) {
        if (!this.notebookTracker.currentWidget) {
            return [];
        }
        const codeCells = [];
        notebook = notebook || this.notebookTracker.currentWidget.content;
        notebook.widgets.forEach((cell) => {
            if (cell.model.type === 'code') {
                if (!selectedOnly || (notebook === null || notebook === void 0 ? void 0 : notebook.isSelectedOrActive(cell))) {
                    codeCells.push(cell);
                }
            }
        });
        return codeCells;
    }
    tryReplacing(cellText, extractor) {
        const extracted = extractor.extract_foreign_code(cellText);
        if (extracted &&
            extracted.length > 0 &&
            extracted[0].foreign_code &&
            extracted[0].range) {
            const sqlText = extracted[0].foreign_code;
            const formattedSql = this.sqlFormatter.format(sqlText) + '\n';
            const doc = new this.codeMirror.CodeMirror.Doc(cellText, 'sql', 0, '\n');
            const startPos = new this.codeMirror.CodeMirror.Pos(extracted[0].range.start.line, extracted[0].range.start.column);
            const endPos = new this.codeMirror.CodeMirror.Pos(extracted[0].range.end.line, extracted[0].range.end.column);
            doc.replaceRange(formattedSql, startPos, endPos);
            return doc.getValue();
        }
        return null;
    }
    async formatCells(selectedOnly, notebook) {
        if (this.working || !this.applicable()) {
            return;
        }
        try {
            this.working = true;
            const selectedCells = this.getCodeCells(selectedOnly, notebook);
            if (selectedCells.length > 0) {
                const currentTexts = selectedCells.map(cell => cell.model.value.text);
                const formattedTexts = currentTexts.map(cellText => {
                    const formatted = this.extractors
                        .map(extractor => this.tryReplacing(cellText, extractor))
                        .find(formatted => formatted);
                    return formatted || '';
                });
                for (let i = 0; i < selectedCells.length; ++i) {
                    const cell = selectedCells[i];
                    const currentText = currentTexts[i];
                    const formattedText = formattedTexts[i];
                    if (cell.model.value.text === currentText) {
                        cell.model.value.text = formattedText;
                    }
                }
            }
        }
        catch (error) {
            await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)('Jupyterlab Code Formatter Error', error);
        }
        finally {
            this.working = false;
        }
    }
    applicable() {
        const selectedCells = this.getCodeCells();
        if (selectedCells.length > 0) {
            const currentTexts = selectedCells.map(cell => cell.model.value.text);
            let numSqlCells = 0;
            currentTexts.forEach(cellText => {
                const found = this.extractors.find(extractor => extractor.has_foreign_code(cellText));
                if (found) {
                    numSqlCells++;
                }
            });
            // eslint-disable-next-line eqeqeq
            return numSqlCells == selectedCells.length;
        }
        return false;
    }
}
class JupyterlabFileEditorCodeFormatter {
    constructor(editorTracker, sqlFormatter) {
        this.working = false;
        this.editorTracker = editorTracker;
        this.sqlFormatter = sqlFormatter;
    }
    setFormatter(sqlFormatter) {
        this.sqlFormatter = sqlFormatter;
    }
    formatAction() {
        if (this.working) {
            return;
        }
        const editorWidget = this.editorTracker.currentWidget;
        if (editorWidget) {
            try {
                this.working = true;
                const editor = editorWidget.content.editor;
                const code = editor === null || editor === void 0 ? void 0 : editor.model.value.text;
                const formatted = this.sqlFormatter.format(code);
                editorWidget.content.editor.model.value.text = formatted;
            }
            finally {
                this.working = false;
            }
        }
    }
}
class JupyterLabCodeFormatter {
    constructor(app, tracker, editorTracker, codeMirror, sqlFormatter) {
        this.app = app;
        this.tracker = tracker;
        this.editorTracker = editorTracker;
        this.notebookCodeFormatter = new JupyterlabNotebookCodeFormatter(this.tracker, codeMirror, sqlFormatter);
        this.fileEditorCodeFormatter = new JupyterlabFileEditorCodeFormatter(this.editorTracker, sqlFormatter);
        this.setupCommands();
        this.setupContextMenu();
    }
    setFormatter(sqlFormatter) {
        this.notebookCodeFormatter.setFormatter(sqlFormatter);
        this.fileEditorCodeFormatter.setFormatter(sqlFormatter);
    }
    setupContextMenu() {
        this.app.contextMenu.addItem({
            command: _constants__WEBPACK_IMPORTED_MODULE_3__.Constants.FORMAT_COMMAND,
            selector: '.jp-CodeCell'
        });
        this.app.contextMenu.addItem({
            command: _constants__WEBPACK_IMPORTED_MODULE_3__.Constants.FORMAT_COMMAND_DOCUMENT,
            selector: '.jp-FileEditor'
        });
    }
    setupCommands() {
        this.app.commands.addCommand(_constants__WEBPACK_IMPORTED_MODULE_3__.Constants.FORMAT_COMMAND, {
            execute: async () => {
                await this.notebookCodeFormatter.formatSelectedCodeCells();
            },
            isVisible: () => {
                return this.notebookCodeFormatter.applicable();
            },
            label: 'Format SQL Cell'
        });
        this.app.commands.addCommand(_constants__WEBPACK_IMPORTED_MODULE_3__.Constants.FORMAT_COMMAND_DOCUMENT, {
            execute: async () => {
                await this.fileEditorCodeFormatter.formatAction();
            },
            label: 'Format SQL Document'
        });
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyter-lsp/jupyterlab-lsp */ "webpack/sharing/consume/default/@jupyter-lsp/jupyterlab-lsp");
/* harmony import */ var _jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _formatter__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./formatter */ "./lib/formatter.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./constants */ "./lib/constants.js");








/*
Results in

LINE_MAGIC_EXTRACT
(?:^|\n)%sparksql(?: |-c|--cache|-e|--eager|-[a-z] [0-9a-zA-Z/._]+|--[a-zA-Z]+ [0-9a-zA-Z/._]+)*([^\n]*)

CELL_MAGIC_EXTRACT
(?:^|\n)%%sparksql(?: |-c|--cache|-e|--eager|-[a-z] [0-9a-zA-Z/._]+|--[a-zA-Z]+ [0-9a-zA-Z/._]+)*\n([^]*)
*/
/**
 * Code taken from https://github.com/jupyterlab/jupyterlab/blob/master/packages/codemirror/src/codemirror-ipython.ts
 * Modified to support embedded sql syntax
 */
function codeMirrorWithSqlSyntaxHighlightSupport(c) {
    /**
     * Define an IPython codemirror mode.
     *
     * It is a slightly altered Python Mode with a `?` operator.
     */
    c.CodeMirror.defineMode('ipython', (config, modeOptions) => {
        const pythonConf = {};
        for (const prop in modeOptions) {
            if (modeOptions.hasOwnProperty(prop)) {
                pythonConf[prop] = modeOptions[prop];
            }
        }
        pythonConf.name = 'python';
        pythonConf.singleOperators = new RegExp('^[\\+\\-\\*/%&|@\\^~<>!\\?]');
        pythonConf.identifiers = new RegExp('^[_A-Za-z\u00A1-\uFFFF][_A-Za-z0-9\u00A1-\uFFFF]*');
        //return c.CodeMirror.getMode(config, pythonConf);
        // Instead of returning this mode we multiplex it with SQL
        const pythonMode = c.CodeMirror.getMode(config, pythonConf);
        // get a mode for SQL
        const sqlMode = c.CodeMirror.getMode(config, 'sql');
        // multiplex python with SQL and return it
        const multiplexedModes = (0,_utils__WEBPACK_IMPORTED_MODULE_5__.sqlCodeMirrorModesFor)('sparksql', sqlMode).concat((0,_utils__WEBPACK_IMPORTED_MODULE_5__.sqlCodeMirrorModesFor)('trino', sqlMode));
        return c.CodeMirror.multiplexingMode(pythonMode, ...multiplexedModes);
    }
    // Original code has a third argument. Not sure why we don't..
    // https://github.com/jupyterlab/jupyterlab/blob/master/packages/codemirror/src/codemirror-ipython.ts
    // ,
    // 'python'
    );
    // The following is already done by default implementation so not redoing here
    // c.CodeMirror.defineMIME('text/x-ipython', 'ipython');
    // c.CodeMirror.modeInfo.push({
    //   ext: [],
    //   mime: 'text/x-ipython',
    //   mode: 'ipython',
    //   name: 'ipython'
    // });
}
/**
 * Initialization data for the jupyterlab-sql-editor extension.
 */
const plugin = {
    id: 'jupyterlab-sql-editor:plugin',
    autoStart: true,
    optional: [],
    requires: [
        _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.ICodeMirror,
        _jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1__.ILSPCodeExtractorsManager,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry,
        _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_4__.IEditorTracker,
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker
    ],
    activate: (app, codeMirror, lspExtractorsMgr, settingRegistry, editorTracker, tracker) => {
        console.log('JupyterLab extension jupyterlab-sql-editor is activated!');
        const sqlFormatter = new _formatter__WEBPACK_IMPORTED_MODULE_6__.SqlFormatter(4, false, 'upper');
        const sqlCodeFormatter = new _formatter__WEBPACK_IMPORTED_MODULE_6__.JupyterLabCodeFormatter(app, tracker, editorTracker, codeMirror, sqlFormatter);
        console.log('jupyterlab-sql-editor SQL code formatter registered');
        /**
         * Load the settings for this extension
         *
         * @param setting Extension settings
         */
        function loadSetting(settings) {
            // Read the settings and convert to the correct type
            const formatTabwidth = settings.get('formatTabWidth').composite;
            const formatUseTabs = settings.get('formatUseTabs').composite;
            const formatKeywordCase = settings.get('formatKeywordCase')
                .composite;
            const sqlFormatter = new _formatter__WEBPACK_IMPORTED_MODULE_6__.SqlFormatter(formatTabwidth, formatUseTabs, formatKeywordCase);
            sqlCodeFormatter.setFormatter(sqlFormatter);
        }
        // Wait for the application to be restored and
        // for the settings for this plugin to be loaded
        Promise.all([
            app.restored,
            settingRegistry.load(_constants__WEBPACK_IMPORTED_MODULE_7__.Constants.SETTINGS_SECTION)
        ])
            .then(([, settings]) => {
            // Read the settings
            loadSetting(settings);
            // Listen for your plugin setting changes using Signal
            settings.changed.connect(loadSetting);
        })
            .catch(reason => {
            console.error(`Something went wrong when reading the settings.\n${reason}`);
        });
        // JupyterLab uses the CodeMirror library to syntax highlight code
        // within the cells. Register a multiplex CodeMirror capable of
        // highlightin SQL which is embedded in a IPython magic or within
        // a python string (delimited by markers)
        codeMirrorWithSqlSyntaxHighlightSupport(codeMirror);
        console.log('jupyterlab-sql-editor code mirror for syntax highlighting registered');
        // JupyterLab-LSP relies on extractors to pull the SQL out of the cell
        // and into a virtual document which is then passed to the sql-language-server
        // for code completion evaluation
        lspExtractorsMgr.register((0,_utils__WEBPACK_IMPORTED_MODULE_5__.markerExtractor)('sparksql'), 'python');
        lspExtractorsMgr.register((0,_utils__WEBPACK_IMPORTED_MODULE_5__.lineMagicExtractor)('sparksql'), 'python');
        lspExtractorsMgr.register((0,_utils__WEBPACK_IMPORTED_MODULE_5__.cellMagicExtractor)('sparksql'), 'python');
        lspExtractorsMgr.register((0,_utils__WEBPACK_IMPORTED_MODULE_5__.markerExtractor)('trino'), 'python');
        lspExtractorsMgr.register((0,_utils__WEBPACK_IMPORTED_MODULE_5__.lineMagicExtractor)('trino'), 'python');
        lspExtractorsMgr.register((0,_utils__WEBPACK_IMPORTED_MODULE_5__.cellMagicExtractor)('trino'), 'python');
        console.log('jupyterlab-sql-editor LSP extractors registered');
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   cellMagicExtractor: () => (/* binding */ cellMagicExtractor),
/* harmony export */   lineMagicExtractor: () => (/* binding */ lineMagicExtractor),
/* harmony export */   markerExtractor: () => (/* binding */ markerExtractor),
/* harmony export */   registerCodeMirrorFor: () => (/* binding */ registerCodeMirrorFor),
/* harmony export */   sqlCodeMirrorModesFor: () => (/* binding */ sqlCodeMirrorModesFor)
/* harmony export */ });
/* harmony import */ var _jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-lsp/jupyterlab-lsp */ "webpack/sharing/consume/default/@jupyter-lsp/jupyterlab-lsp");
/* harmony import */ var _jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__);

function line_magic(language) {
    return `%${language}`;
}
function cell_magic(language) {
    return `%%${language}`;
}
function start(language) {
    return `--start-${language}`;
}
function end(language) {
    return `--end-${language}`;
}
// sparksql magic accepts options in the long form
// --dataframe df
// or in the short form
// -d df
// some options do not require any values, they act more as a flag
const SPACE = ' ';
const OPTION_VALUE = '[0-9a-zA-Z\\._]+';
const SHORT_OPTS = '-[a-z]';
const LONG_OPTS = '--[_a-zA-Z]+';
const COMMANDS = `(?:${SPACE}|${SHORT_OPTS} ${OPTION_VALUE}|${LONG_OPTS} ${OPTION_VALUE}|${SHORT_OPTS}|${LONG_OPTS})*`;
const BEGIN = '(?:^|\n)';
function sqlCodeMirrorModesFor(language, sqlMode) {
    return [
        {
            open: `${start(language)}`,
            close: `${end(language)}`,
            // parseDelimiters is set to true which considers
            // the marker as part of the SQL statement
            // it is thus syntax highlighted as a comment
            parseDelimiters: true,
            mode: sqlMode
        },
        {
            open: RegExp(`${line_magic(language)}${COMMANDS}`),
            close: '\n',
            parseDelimiters: false,
            mode: sqlMode
        },
        {
            open: RegExp(`${cell_magic(language)}${COMMANDS}`),
            close: '__A MARKER THAT WILL NEVER BE MATCHED__',
            parseDelimiters: false,
            mode: sqlMode
        }
    ];
}
function lineMagicExtractor(language) {
    return new _jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.RegExpForeignCodeExtractor({
        language: language,
        pattern: `${BEGIN}${line_magic(language)}${COMMANDS}([^\n]*)`,
        foreign_capture_groups: [1],
        is_standalone: true,
        file_extension: language
    });
}
function cellMagicExtractor(language) {
    return new _jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.RegExpForeignCodeExtractor({
        language: language,
        pattern: `^${cell_magic(language)}.*?\n([\\S\\s]*)`,
        foreign_capture_groups: [1],
        is_standalone: true,
        file_extension: language
    });
}
function markerExtractor(language) {
    return new _jupyter_lsp_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.RegExpForeignCodeExtractor({
        language: language,
        pattern: `${start(language)}.*?\n([\\S\\s]*)${end(language)}`,
        foreign_capture_groups: [1],
        is_standalone: true,
        file_extension: language
    });
}
/**
 * Register text editor based on file type.
 * @param c
 * @param language
 */
function registerCodeMirrorFor(c, language) {
    c.CodeMirror.defineMode(language, (config, modeOptions) => {
        const mode = c.CodeMirror.getMode(config, 'sql');
        return mode;
    });
    c.CodeMirror.defineMIME(`text/x-${language}`, language);
    c.CodeMirror.modeInfo.push({
        ext: [language],
        mime: `text/x-${language}`,
        mode: language,
        name: language
    });
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.8929786c7d1c48de2033.js.map