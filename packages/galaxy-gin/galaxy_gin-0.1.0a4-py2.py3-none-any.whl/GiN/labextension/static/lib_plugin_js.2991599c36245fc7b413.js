"use strict";
(self["webpackChunkGiN"] = self["webpackChunkGiN"] || []).push([["lib_plugin_js"],{

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _g2nb_nbtools_lib_dataregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @g2nb/nbtools/lib/dataregistry */ "./node_modules/@g2nb/nbtools/lib/dataregistry.js");
/* harmony import */ var _g2nb_nbtools__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @g2nb/nbtools */ "webpack/sharing/consume/default/@g2nb/nbtools/@g2nb/nbtools");
/* harmony import */ var _g2nb_nbtools__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_g2nb_nbtools__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _g2nb_nbtools_lib_context__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @g2nb/nbtools/lib/context */ "./node_modules/@g2nb/nbtools/lib/context.js");
/* harmony import */ var _Galaxyuibuilder__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./Galaxyuibuilder */ "./lib/Galaxyuibuilder.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _version__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./version */ "./lib/version.js");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _notebookActions__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./notebookActions */ "./lib/notebookActions.js");






// import { ContextManager } from '@g2nb/nbtools';






// import {refresh_cells} from './Galaxyuibuilder';




const module_exports = Object.assign(Object.assign(Object.assign({},  _Galaxyuibuilder__WEBPACK_IMPORTED_MODULE_7__), _utils__WEBPACK_IMPORTED_MODULE_8__));

const EXTENSION_ID = 'GiN:plugin';
/**
 * The example plugin.
 */
 const galaxy_plugin = {
    id: EXTENSION_ID,
    //provides: IGalaxyTool,
    requires: [_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__.IJupyterWidgetRegistry],
    optional: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILayoutRestorer, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker],
    activate: activateWidgetExtension,
    autoStart: true,
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (galaxy_plugin);
/**
 * Activate the widget extension.
 * 
 */
function activateWidgetExtension(app, registry, mainmenu, restorer, shell, notebook_tracker) {

    init_context(app, notebook_tracker)

    // const data_registry = new DataRegistry();
    const tool_registry = new _g2nb_nbtools__WEBPACK_IMPORTED_MODULE_5__.ToolRegistry();
    const data_registry = new _g2nb_nbtools_lib_dataregistry__WEBPACK_IMPORTED_MODULE_4__.DataRegistry();

    registry.registerWidget({
        name: 'GiN',
        version: '0.1.0',
        exports: module_exports,
    });
    return [tool_registry, data_registry]
}

function init_context(app, notebook_tracker) {
    _g2nb_nbtools_lib_context__WEBPACK_IMPORTED_MODULE_6__.ContextManager.jupyter_app = app;
    _g2nb_nbtools_lib_context__WEBPACK_IMPORTED_MODULE_6__.ContextManager.notebook_tracker = notebook_tracker;
    _g2nb_nbtools_lib_context__WEBPACK_IMPORTED_MODULE_6__.ContextManager.context();
    notebook_tracker

    initNotebookTracker(notebook_tracker)
    
}



function ReturnOutputArea(i, notebookTracker){
    var RestorForm = `<div class="lm-Widget p-Widget lm-Panel p-Panel jp-OutputArea-child">
                        <div class="lm-Widget p-Widget jp-OutputPrompt jp-OutputArea-prompt"></div>
                        <div class="lm-Widget p-Widget lm-Panel p-Panel jupyter-widgets jp-OutputArea-output">${i}</div>
                    </div>`

                    const utm = new DOMParser().parseFromString(RestorForm, 'text/html').querySelector('.lm-Widget.p-Widget.lm-Panel.p-Panel.jp-OutputArea-child')
    
    const notebook = notebookTracker.currentWidget.content
    const notebookHasBeenRan = (0,_notebookActions__WEBPACK_IMPORTED_MODULE_11__.getRanNotebookIds)().includes(notebook.id)

    _.each(utm.querySelectorAll('.nbtools-run'), (e)=>{
        e.innerText = "Update form for current user"

        e.addEventListener('click', async () => {
            // if ( notebookHasBeenRan === false) {

                const notebookContext = notebookTracker.currentWidget.context;
                const notebookSession = notebookTracker.currentWidget.context.sessionContext;

                notebookTracker.currentWidget.sessionContext.ready
                    .then(() => notebookTracker.currentWidget.revealed)
                    .then(() => {
                        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookActions.run(notebook, notebookSession);
                });
                e.parentNode.parentNode.parentNode.parentNode.parentNode.parentElement.removeChild(e.parentNode.parentNode.parentNode.parentNode.parentNode)
            // }
        })
    })

    return utm
}


const initNotebookTracker = (notebookTracker) => {

    const notebookHasBeenRan = (0,_notebookActions__WEBPACK_IMPORTED_MODULE_11__.getRanNotebookIds)()

    notebookTracker.currentChanged.connect((notebookTracker, notebookPanel) => {
        if (!notebookTracker.currentWidget) {
            return;
        }
        const notebookContext = notebookTracker.currentWidget.context;

        notebookContext.ready.then(() => {

            const notebook = notebookTracker.currentWidget.content;
            const notebookSession = notebookTracker.currentWidget.context.sessionContext;
        
            if ( notebookHasBeenRan.includes(notebook.id) === false) {
            //FixME Form Restore insteed cell run

                _notebookActions__WEBPACK_IMPORTED_MODULE_11__.Private.ranNotebookIds.push(notebook.id);
            
                notebookTracker.currentWidget.sessionContext.ready.then(() =>
                notebookTracker.currentWidget.revealed).then(async () => {

                var cells = notebookTracker.currentWidget.content.widgets;

                for (var i = 0; i < cells.length; i++){
                    if (cells[i].model.metadata.get('galaxy_cell') ){
                        if (cells[i].model.metadata.get('html') == undefined || cells[i].model.metadata.get('html') == '') {
                            (0,_utils__WEBPACK_IMPORTED_MODULE_8__.removeAllChildNodes)(cells[i].outputArea.node)
                            notebook.activeCellIndex = i
                            await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.NotebookActions.run(notebook, notebookSession);            
                       
                        } else{
                            // cells[i].inputArea.hide()
                            (0,_utils__WEBPACK_IMPORTED_MODULE_8__.removeAllChildNodes)(cells[i].outputArea.node)
                            cells[i].outputArea.node.append(ReturnOutputArea(cells[i].model.metadata.get('html'), notebookTracker))
                        }
                    }
                 }
            });

            }
        });
    });
};

/***/ })

}]);
//# sourceMappingURL=lib_plugin_js.2991599c36245fc7b413.js.map