"use strict";
(self["webpackChunkcognite_jupyterlab_metrics"] = self["webpackChunkcognite_jupyterlab_metrics"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   cogniteMetrics: () => (/* binding */ cogniteMetrics),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);



/**
 * A plugin that sends notebook events to Fusion.
 */
const cogniteMetrics = {
    id: 'cognite_jupyterlab_metrics:plugin',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry],
    activate: (app, nbTracker, manager, settingRegistry) => {
        // Try to read the settings so that the cell toolbar updates
        if (settingRegistry) {
            void settingRegistry.load('@jupyterlab/comments-extension:notebook');
        }
        const executedCode = {};
        let currentNotebook = undefined;
        const track = (eventName, data) => {
            window.parent.postMessage({
                event: 'jupyterliteEvent',
                data: { eventName, data }
            }, '*');
        };
        window.nbTracker = nbTracker;
        nbTracker.currentChanged.connect((sender, notebook) => {
            const notebookTitle = (notebook === null || notebook === void 0 ? void 0 : notebook.context)._path;
            currentNotebook = notebookTitle;
            track('jupyterLiteNotebookChanged', { notebookTitle });
        });
        nbTracker.activeCellChanged.connect((sender, cell) => {
            track('jupyterLiteActiveCellChanged', {});
        });
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.NotebookActions.executed.connect((sender, args) => {
            const { cell } = args;
            // console.log('Cell: ', cell);
            window.cell = cell;
            const cellModel = cell.model.toJSON();
            window.cellModel = cellModel;
            console.log('Cell model: ', cellModel);
            const executionCount = cellModel.execution_count;
            const code = cellModel.source;
            const cellType = cellModel.cell_type;
            const outputs = cellModel.outputs;
            const anyErrors = outputs.some((output) => output.output_type === 'error');
            if (currentNotebook === undefined) {
                return;
            }
            if (executedCode[currentNotebook] === undefined) {
                executedCode[currentNotebook] = [];
            }
            executedCode[currentNotebook].push(code);
            track('jupyterLiteCellExecuted', {
                cellType,
                executionCount,
                code,
                success: !anyErrors
            });
            if (anyErrors) {
                const errorOutput = outputs.find((output) => output.output_type === 'error');
                const errorName = errorOutput.ename;
                const errorValue = errorOutput.evalue;
                const errorTraceback = errorOutput.traceback.join('\n');
                track('jupyterLiteCellError', {
                    cellType,
                    executionCount,
                    code,
                    errorName,
                    errorValue,
                    errorTraceback,
                    executedCode: executedCode[currentNotebook]
                });
            }
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (cogniteMetrics);
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=lib_index_js.f1f6a0d009883b94d4a5.js.map