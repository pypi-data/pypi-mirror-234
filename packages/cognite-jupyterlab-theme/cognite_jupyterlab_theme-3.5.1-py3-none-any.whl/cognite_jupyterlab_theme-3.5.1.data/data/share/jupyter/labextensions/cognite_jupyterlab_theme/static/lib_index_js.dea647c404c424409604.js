"use strict";
(self["webpackChunkcognite_jupyterlab_theme"] = self["webpackChunkcognite_jupyterlab_theme"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * Initialization data for the cognite_jupyterlab_theme extension.
 */
const plugin = {
    id: 'cognite_jupyterlab_theme:plugin',
    description: 'A JupyterLab extension adding a Cognite theme.',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    activate: (app, manager) => {
        console.log('JupyterLab extension cognite_jupyterlab_theme is activated!');
        manager.register({
            name: 'Cognite',
            isLight: true,
            load: () => manager.loadCSS('cognite_jupyterlab_theme/index.css'),
            unload: () => Promise.resolve(undefined)
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=lib_index_js.dea647c404c424409604.js.map