"use strict";
(self["webpackChunkcell_toolbar"] = self["webpackChunkcell_toolbar"] || []).push([["lib_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `.jp-Cell .ccb-cellFooterContainer {
   display: flex;
   flex-direction: row; /* Ensure horizontal alignment */
   justify-content: flex-start; /* Move button to the left */
   align-items: center; /* Vertically center the button */
  }

  .jp-Cell .ccb-cellFooterBtn {
    color: #fff;
    opacity: 0.7;
    font-size: 0.65rem;
    font-weight: 500;
    text-transform: uppercase;
    border: none;
    padding: 4px 8px;
    margin: 0.2rem 0;
    text-shadow: 0px 0px 5px rgba(0, 0, 0, 0.15);
    outline: none;
    cursor: pointer;
    user-select: none;  
    margin-left: 0px;
    margin-right: 4px;
  }

  .jp-Placeholder-content .jp-PlaceholderText,
  .jp-Placeholder-content .jp-MoreHorizIcon {
    display: none;
  }

  /* Disable default cell collapsing behavior */
.jp-InputCollapser,
.jp-OutputCollapser,
.jp-Placeholder {
  cursor: auto !important;
  pointer-events: none !important;
}

  /* Add styles for toggle button */
  .jp-Cell .ccb-toggleBtn{
    background: #f0f0f0;
  }

  .jp-Cell .ccb-toggleBtn:hover{
    background-color: #ccc;
  }

  .jp-Cell .ccb-toggleBtn:active{
    background-color: #999;
  }
  
  .jp-Cell .ccb-cellFooterBtn:active {
    background-color: var(--md-blue-600);
    text-shadow: 0px 0px 4px rgba(0, 0, 0, 0.4);
  }
  
  .jp-Cell .ccb-cellFooterBtn:hover {
    background-color: var(--md-blue-500);
    opacity: 1;
    text-shadow: 0px 0px 7px rgba(0, 0, 0, 0.3);
    box-shadow: var(--jp-elevation-z2);
  }
  
  .jp-Cell .ccb-cellFooterBtn {
    background: var(--md-blue-400);
  }
  
  .jp-CodeCell {
    display: flex !important;
    flex-direction: column;
  }
  
  .jp-CodeCell .jp-CellFooter {
    height: auto;
    order: 2;
  }
  
  .jp-Cell .jp-Cell-inputWrapper {
    margin-top: 5px;
  }
  
  .jp-CodeCell .jp-Cell-outputWrapper {
    order: 4;
  }
  `, "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":"AAAA;GACG,aAAa;GACb,mBAAmB,EAAE,gCAAgC;GACrD,2BAA2B,EAAE,4BAA4B;GACzD,mBAAmB,EAAE,iCAAiC;EACvD;;EAEA;IACE,WAAW;IACX,YAAY;IACZ,kBAAkB;IAClB,gBAAgB;IAChB,yBAAyB;IACzB,YAAY;IACZ,gBAAgB;IAChB,gBAAgB;IAChB,4CAA4C;IAC5C,aAAa;IACb,eAAe;IACf,iBAAiB;IACjB,gBAAgB;IAChB,iBAAiB;EACnB;;EAEA;;IAEE,aAAa;EACf;;EAEA,6CAA6C;AAC/C;;;EAGE,uBAAuB;EACvB,+BAA+B;AACjC;;EAEE,iCAAiC;EACjC;IACE,mBAAmB;EACrB;;EAEA;IACE,sBAAsB;EACxB;;EAEA;IACE,sBAAsB;EACxB;;EAEA;IACE,oCAAoC;IACpC,2CAA2C;EAC7C;;EAEA;IACE,oCAAoC;IACpC,UAAU;IACV,2CAA2C;IAC3C,kCAAkC;EACpC;;EAEA;IACE,8BAA8B;EAChC;;EAEA;IACE,wBAAwB;IACxB,sBAAsB;EACxB;;EAEA;IACE,YAAY;IACZ,QAAQ;EACV;;EAEA;IACE,eAAe;EACjB;;EAEA;IACE,QAAQ;EACV","sourcesContent":[".jp-Cell .ccb-cellFooterContainer {\n   display: flex;\n   flex-direction: row; /* Ensure horizontal alignment */\n   justify-content: flex-start; /* Move button to the left */\n   align-items: center; /* Vertically center the button */\n  }\n\n  .jp-Cell .ccb-cellFooterBtn {\n    color: #fff;\n    opacity: 0.7;\n    font-size: 0.65rem;\n    font-weight: 500;\n    text-transform: uppercase;\n    border: none;\n    padding: 4px 8px;\n    margin: 0.2rem 0;\n    text-shadow: 0px 0px 5px rgba(0, 0, 0, 0.15);\n    outline: none;\n    cursor: pointer;\n    user-select: none;  \n    margin-left: 0px;\n    margin-right: 4px;\n  }\n\n  .jp-Placeholder-content .jp-PlaceholderText,\n  .jp-Placeholder-content .jp-MoreHorizIcon {\n    display: none;\n  }\n\n  /* Disable default cell collapsing behavior */\n.jp-InputCollapser,\n.jp-OutputCollapser,\n.jp-Placeholder {\n  cursor: auto !important;\n  pointer-events: none !important;\n}\n\n  /* Add styles for toggle button */\n  .jp-Cell .ccb-toggleBtn{\n    background: #f0f0f0;\n  }\n\n  .jp-Cell .ccb-toggleBtn:hover{\n    background-color: #ccc;\n  }\n\n  .jp-Cell .ccb-toggleBtn:active{\n    background-color: #999;\n  }\n  \n  .jp-Cell .ccb-cellFooterBtn:active {\n    background-color: var(--md-blue-600);\n    text-shadow: 0px 0px 4px rgba(0, 0, 0, 0.4);\n  }\n  \n  .jp-Cell .ccb-cellFooterBtn:hover {\n    background-color: var(--md-blue-500);\n    opacity: 1;\n    text-shadow: 0px 0px 7px rgba(0, 0, 0, 0.3);\n    box-shadow: var(--jp-elevation-z2);\n  }\n  \n  .jp-Cell .ccb-cellFooterBtn {\n    background: var(--md-blue-400);\n  }\n  \n  .jp-CodeCell {\n    display: flex !important;\n    flex-direction: column;\n  }\n  \n  .jp-CodeCell .jp-CellFooter {\n    height: auto;\n    order: 2;\n  }\n  \n  .jp-Cell .jp-Cell-inputWrapper {\n    margin-top: 5px;\n  }\n  \n  .jp-CodeCell .jp-Cell-outputWrapper {\n    order: 4;\n  }\n  "],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CellFooterWithButton: () => (/* binding */ CellFooterWithButton),
/* harmony export */   ContentFactoryWithFooterButton: () => (/* binding */ ContentFactoryWithFooterButton),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");
// Import necessary dependencies from React, JupyterLab, and other modules





/**
 * Define CSS classes used in the cell footer.
 */
const CELL_FOOTER_CLASS = 'jp-CellFooter';
const CELL_FOOTER_DIV_CLASS = 'ccb-cellFooterContainer';
const CELL_FOOTER_BUTTON_CLASS = 'ccb-cellFooterBtn';
const CELL_TOGGLE_BUTTON_CLASS = '.ccb-toggleBtn';
// Function to activate custom commands
function activateCommands(app, tracker) {
    // Output a message to the console to indicate activation
    console.log('JupyterLab extension jupyterlab-aaVisualPolish is activated!');
    // Wait for the app to be restored before proceeding
    Promise.all([app.restored]).then(([params]) => {
        const { commands, shell } = app;
        // Function to get the current NotebookPanel
        function getCurrent(args) {
            const widget = tracker.currentWidget;
            const activate = args.activate !== false;
            if (activate && widget) {
                shell.activateById(widget.id);
            }
            return widget;
        }
        /**
        * Function to check if the command should be enabled.
        * It checks if there is a current notebook widget and if it matches the app's current widget.
        * If both conditions are met, the command is considered enabled.
        */
        function isEnabled() {
            return (tracker.currentWidget !== null &&
                tracker.currentWidget === app.shell.currentWidget);
        }
        // Define a command to hide the code in the current cell
        commands.addCommand('hide-cell-code', {
            label: 'Hide Cell',
            execute: args => {
                const current = getCurrent(args);
                if (current) {
                    const { content } = current;
                    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookActions.hideCode(content);
                }
            },
            isEnabled
        });
        // Define a command to show the code in the current cell
        commands.addCommand('show-cell-code', {
            label: 'Show Cell',
            execute: args => {
                const current = getCurrent(args);
                if (current) {
                    const { content } = current;
                    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookActions.showCode(content);
                }
            },
            isEnabled
        });
        // Define a command to run the code in the current cell
        commands.addCommand('run-selected-codecell', {
            label: 'Run Cell',
            execute: args => {
                const current = getCurrent(args);
                if (current) {
                    const { context, content } = current;
                    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookActions.run(content, context.sessionContext);
                }
            },
            isEnabled
        });
    });
    //Event listener to collapse code cells when a notebook is loaded
    tracker.widgetAdded.connect((sender, panel) => {
        function collapseAllCodeCells(panel) {
            const { content } = panel;
            const cells = content.widgets;
            cells.forEach(cell => {
                if (cell.model.type === 'code') {
                    _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookActions.hideAllCode(panel.content);
                }
            });
        }
        // Collapse code cells when the current notebook is loaded
        panel.context.ready.then(() => {
            collapseAllCodeCells(panel);
        });
    });
    return Promise.resolve();
}
/**
 * Extend the default implementation of an `IContentFactory`.
 */
class ContentFactoryWithFooterButton extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookPanel.ContentFactory {
    constructor(commands, options) {
        super(options);
        this.commands = commands;
    }
    /**
     * Create a new cell header for the parent widget.
     */
    createCellFooter() {
        return new CellFooterWithButton(this.commands);
    }
}
/**
 * Extend the default implementation of a cell footer with custom buttons.
 */
class CellFooterWithButton extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(commands) {
        super();
        this.RUN_ICON = 'fas fa-play-circle';
        this.addClass(CELL_FOOTER_CLASS);
        this.commands = commands;
        this.codeVisible = false;
        // Add an event listener to the blue bar element
        this.node.addEventListener('click', (event) => {
            // Prevent the default behavior (collapsing/expanding)
            event.preventDefault();
        });
    }
    render() {
        console.log('Rendering element');
        const toggleIcon = this.codeVisible ? 'fas fa-eye-slash' : 'fas fa-eye';
        return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: CELL_FOOTER_DIV_CLASS }, react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", {
            className: CELL_FOOTER_BUTTON_CLASS,
            onClick: () => {
                console.log("Clicked run cell");
                this.commands.execute('run-selected-codecell');
            },
        }, react__WEBPACK_IMPORTED_MODULE_0__.createElement("i", { className: this.RUN_ICON })), react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", {
            className: `${CELL_FOOTER_BUTTON_CLASS} ${CELL_TOGGLE_BUTTON_CLASS}`,
            onClick: () => {
                console.log("Clicked toggle cell visibility");
                this.codeVisible = !this.codeVisible;
                if (this.codeVisible) {
                    this.commands.execute('show-cell-code');
                }
                else {
                    this.commands.execute('hide-cell-code');
                }
                this.update();
            },
        }, react__WEBPACK_IMPORTED_MODULE_0__.createElement("i", { className: toggleIcon })));
    }
}
/**
 * Define a JupyterLab extension to add footer buttons to code cells.
 */
const footerButtonExtension = {
    id: 'jupyterlab-aaVisualPolish',
    autoStart: true,
    activate: activateCommands,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker]
};
/**
 * Define a JupyterLab extension to override the default notebook cell factory.
 */
const cellFactory = {
    id: 'jupyterlab-aaVisualPolish:factory',
    provides: _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookPanel.IContentFactory,
    requires: [_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorServices],
    autoStart: true,
    activate: (app, editorServices) => {
        // tslint:disable-next-line:no-console
        console.log('JupyterLab extension jupyterlab-aaVisualPolish', 'overrides default nootbook content factory');
        const { commands } = app;
        const editorFactory = editorServices.factoryService.newInlineEditor;
        return new ContentFactoryWithFooterButton(commands, { editorFactory });
    }
};
/**
 * Export this plugins as default.
 */
const plugins = [
    footerButtonExtension,
    cellFactory
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.1b13a7f88c52aff8b7f7.js.map