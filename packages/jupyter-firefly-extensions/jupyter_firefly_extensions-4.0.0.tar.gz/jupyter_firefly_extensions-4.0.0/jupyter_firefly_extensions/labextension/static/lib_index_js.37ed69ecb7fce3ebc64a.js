"use strict";
(self["webpackChunkjupyter_firefly_extensions"] = self["webpackChunkjupyter_firefly_extensions"] || []).push([["lib_index_js"],{

/***/ "./lib/FireflyCommonUtils.js":
/*!***********************************!*\
  !*** ./lib/FireflyCommonUtils.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   buildURLErrorHtml: () => (/* binding */ buildURLErrorHtml),
/* harmony export */   findFirefly: () => (/* binding */ findFirefly),
/* harmony export */   makeLabEndpoint: () => (/* binding */ makeLabEndpoint)
/* harmony export */ });
/* harmony import */ var firefly_api_access__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! firefly-api-access */ "webpack/sharing/consume/default/firefly-api-access/firefly-api-access");
/* harmony import */ var firefly_api_access__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(firefly_api_access__WEBPACK_IMPORTED_MODULE_0__);

let cachedLoc;
let cachedFindFireflyResult;
const ffLocURL = makeLabEndpoint('lab/fireflyLocation');
const fetchOptions = {
    method: 'get',
    mode: 'cors',
    credentials: 'include',
    cache: 'default',
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
};
/**
 * Determine where firefly is my calling the lab server extension then load firefly.
 * Results are cache so this function can be call many times.
 * @return {Promise<{firefly: Object, channel: string, fireflyURL: string}>}
 */
async function findFirefly() {
    var _a;
    if (cachedFindFireflyResult)
        return cachedFindFireflyResult;
    try {
        if (!cachedLoc)
            cachedLoc = await (await fetch(ffLocURL, fetchOptions)).json();
        const { fireflyURL = 'http://localhost:8080/firefly', fireflyChannel: channel } = cachedLoc;
        if (!((_a = window.firefly) === null || _a === void 0 ? void 0 : _a.initialized))
            window.firefly = { ...window.firefly, wsch: channel };
        if (!window.getFireflyAPI)
            window.getFireflyAPI = (0,firefly_api_access__WEBPACK_IMPORTED_MODULE_0__.initFirefly)(fireflyURL);
        const firefly = await window.getFireflyAPI();
        cachedFindFireflyResult = { fireflyURL, channel, firefly };
        return cachedFindFireflyResult;
    }
    catch (e) {
        console.group('Firefly Load Failed');
        console.log('findFirefly: Could not determine firefly location or load firefly, call failed');
        console.log(`find firefly url: ${ffLocURL}`);
        if (cachedLoc)
            console.log(`firefly url: ${cachedLoc.fireflyURL} channel: ${cachedLoc.channel}`);
        console.log(e);
        console.groupEnd('Firefly Load Failed');
    }
}
function buildURLErrorHtml(e) {
    const details = `<br>Set the firefly URL by setting <code>c.Firefly.url</code> in 
                    <code>jupyter_notebook_config.py</code>
                    <br>or the environment variable <code>FIREFLY_URL</code>`;
    return `<div style='padding: 30px 0 0 30px'>${e.message}${details}</div>`;
}
function makeLabEndpoint(endPoint, searchParams) {
    const { origin, pathname } = new URL(window.document.location.href);
    const originURL = origin + pathname;
    const start = originURL.substring(0, originURL.lastIndexOf('lab'));
    const slashMaybe = start.endsWith('/') ? '' : '/';
    return `${start}${slashMaybe}${endPoint}${searchParams ? '?' + searchParams.toString() : ''}`;
}


/***/ }),

/***/ "./lib/FitsViewerExt.js":
/*!******************************!*\
  !*** ./lib/FitsViewerExt.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FITS_MIME_TYPE: () => (/* binding */ FITS_MIME_TYPE),
/* harmony export */   FitsViewerWidget: () => (/* binding */ FitsViewerWidget),
/* harmony export */   activateFitsViewerExt: () => (/* binding */ activateFitsViewerExt),
/* harmony export */   createNewFitsViewerDocumentWidget: () => (/* binding */ createNewFitsViewerDocumentWidget)
/* harmony export */ });
/* harmony import */ var b64_to_blob__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! b64-to-blob */ "webpack/sharing/consume/default/b64-to-blob/b64-to-blob");
/* harmony import */ var b64_to_blob__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(b64_to_blob__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./FireflyCommonUtils.js */ "./lib/FireflyCommonUtils.js");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__);





const FITS_MIME_TYPE = 'application/fits';
/**
 * The class name added to the extension.
 */
const CLASS_NAME = 'jp-OutputWidgetFITS';
let idCounter = 0;
const FACTORY = 'FITS-IMAGE';
const fitsIFileType = {
    name: 'FITS',
    displayName: 'FITS file',
    fileFormat: 'base64',
    // will need to check the JL version someway
    format: 'base64',
    mimeTypes: [FITS_MIME_TYPE],
    extensions: ['.fits']
};
/**
 *
 * @param {JupyterLab} app
 * @param {ILayoutRestorer} restorer
 */
function activateFitsViewerExt(app, restorer) {
    var _a;
    const namespace = 'firefly-imageviewer-widget';
    const jlVersion = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.PageConfig.getOption('appVersion');
    const vAry = (_a = jlVersion === null || jlVersion === void 0 ? void 0 : jlVersion.split('.').map((x) => Number(x))) !== null && _a !== void 0 ? _a : [0, 0, 0];
    // if Jupyter Lab version is 3.1 or greater then clear the fileFormat so it does not load the file on the client
    // see - https://github.com/jupyterlab/jupyterlab/pull/7596
    if (vAry[0] >= 3 && vAry[1] >= 1)
        fitsIFileType.fileFormat = null;
    app.docRegistry.addFileType(fitsIFileType);
    const factory = new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.ABCWidgetFactory({
        name: FACTORY,
        modelName: 'base64',
        // modelName: 'fits-model',
        fileTypes: ['FITS'],
        defaultFor: ['FITS'],
        readOnly: true
    });
    factory.createNewWidget = createNewFitsViewerDocumentWidget;
    app.docRegistry.addWidgetFactory(factory);
    factory.widgetCreated.connect((sender, widget) => {
        const types = app.docRegistry.getFileTypesForPath(widget.context.path);
        if (types.length) {
            widget.title.iconClass = types[0].iconClass || '';
            widget.title.iconLabel = types[0].iconLabel || '';
        }
    });
}
function createNewFitsViewerDocumentWidget(context) {
    // instead of extending DocumentWidget like the example, just use it directly
    return new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.DocumentWidget({ content: new FitsViewerWidget(context), context, reveal: true, toolbar: null });
}
/**
 * A widget for rendering FITS.
 */
class FitsViewerWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    /**
     * Construct a new output widget.
     * @param context
     */
    constructor(context) {
        super({ node: createNode(context._path) });
        const useModel = window.firefly && window.firefly.jlExtUseModel || false;
        this.addClass(CLASS_NAME);
        this.filename = context._path;
        idCounter++;
        this.plotId = `${this.filename}-${idCounter}`;
        this.loaded = false;
        if (this.isDisposed)
            return;
        this.renderModel(context, useModel).then(() => {
        });
        context.model.contentChanged.connect(this.renderModel, this);
        context.fileChanged.connect(this.renderModel, this);
    }
    /**
     * Render FITS into this widget's node.
     * @param context
     * @param useModelFirst
     * @return {Promise<{firefly: Object, channel: string, fireflyURL: string}>}
     */
    renderModel(context, useModelFirst) {
        if (this.isDisposed)
            return;
        if (this.loaded) {
            return (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.findFirefly)()
                .then((ffConfig) => ffConfig.firefly.action.dispatchChangeActivePlotView(this.plotId));
        }
        let firefly, fireflyURL;
        return (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.findFirefly)()
            .then((ffConfig) => {
            firefly = ffConfig.firefly;
            fireflyURL = ffConfig.fireflyURL;
            if (useModelFirst) {
                return context.ready.then(() => loadFileToServer(context.model.toString(), this.filename, firefly, fireflyURL));
            }
            else {
                return tellLabToLoadFileToServer(this.filename, firefly);
            }
        })
            .then((response) => response.text())
            .then((text) => {
            if (useModelFirst) {
                const [, cacheKey] = text.split('::::');
                showImage(cacheKey, this.plotId, this.filename, firefly);
            }
            else {
                if (text && text.length < 300 && text.startsWith('${')) {
                    showImage(text, this.plotId, this.filename, firefly);
                }
                else {
                    console.log('Firefly FitsViewExt: Failed to upload from server, ' +
                        'falling back to (slower) browser upload.');
                    context.ready.then(() => loadFileToServer(context.model.toString(), this.filename, firefly, fireflyURL))
                        .then((response) => response.text())
                        .then((text) => {
                        const [, cacheKey] = text.split('::::');
                        showImage(cacheKey, this.plotId, this.filename, firefly);
                    });
                }
            }
            this.loaded = true;
        })
            .catch((e) => {
            const div = document.getElementById(this.filename);
            if (div)
                div.innerHTML = (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.buildURLErrorHtml)(e);
        });
    }
    dispose() {
        return (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.findFirefly)()
            .then((ffConfig) => ffConfig.firefly.action.dispatchDeletePlotView({ plotId: this.plotId, holdWcsMatch: true }));
    }
    activate() {
        super.activate();
        if (this.loaded) {
            return (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.findFirefly)().then((ffConfig) => ffConfig.firefly.action.dispatchChangeActivePlotView(this.plotId));
        }
    }
}
function tellLabToLoadFileToServer(path, firefly) {
    const url = (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.makeLabEndpoint)('lab/sendToFirefly', new URLSearchParams({ 'path': path }));
    return firefly.util.fetchUrl(url, { method: 'GET' }, false, false)
        .catch((e) => {
        console.error('Firefly FitsViewExt: Got Error from upload request', e);
        return 'FAILED';
    });
}
function loadFileToServer(fileData, filename, firefly, fireflyURL) {
    const { fetchUrl, ServerParams } = firefly.util;
    const UL_URL = `${fireflyURL}/sticky/CmdSrv?${ServerParams.COMMAND}=${ServerParams.UPLOAD}&filename=${filename}`;
    const fitsBlob = b64_to_blob__WEBPACK_IMPORTED_MODULE_0___default()(fileData);
    const options = { method: 'multipart', params: { filename, type: 'FITS', file: fitsBlob } };
    return fetchUrl(UL_URL, options);
}
function showImage(cacheKey, plotId, filename, firefly) {
    const req = {
        type: 'FILE',
        FILE: cacheKey,
        plotId,
        plotGroupId: 'JUPLAB',
        title: filename
    };
    firefly.action.dispatchApiToolsView(true, false);
    firefly.setGlobalPref({ imageDisplayType: 'encapusulate' });
    firefly.showImage(filename, req, null, false);
}
function createNode(filename) {
    const node = document.createElement('div');
    node.id = filename;
    return node;
}
//=========================================================================================================
//============ Keep code below for reference
//============ Keep code below for reference
//============ Keep code below for reference
// /**
//  * A mime renderer factory for FITS data.
//  */
// export const fitsViewerRendererFactory = {
//     safe: true,
//     mimeTypes: [FITS_MIME_TYPE],
//     createRenderer: options => {
//         return new FitsViewerWidget (options);
//     }
// };
// import { ABCWidgetFactory, DocumentRegistry, DocumentWidget, IDocumentWidget } from '@jupyterlab/docregistry';
// import { PageConfig, URLExt } from '@jupyterlab/coreutils';
// const ERROR_MSG_CONT= `Make sure you set the firefly URL in your jupyter_notebook_config.py.
//                 For example- 'c.Firefly.url= http://some.firefly.url/firefly'`;
// for adding a second extension for a mime type - does not work yet in Jupyter Lab
// --- https://github.com/jupyterlab/jupyterlab/issues/5381
// export const fitsViewerRendererFactory2 = {
//     safe: true,
//     mimeTypes: [FITS_MIME_TYPE],
//     createRenderer: options => {
//         return new FitsViewerWidget (options);
//     }
// };
// export class FitsViewerDocument extends DocumentWidget {
//
//   constructor(context) {
//       super({ content:new FitsViewerWidget(context), context, reveal:true, toolbar:null });
//     // const toolbar = Private.createToolbar(content.viewer);
//     // const reveal = content.ready;
//   }
// }
// export class FitsViewerFactory extends ABCWidgetFactory {
//
//     constructor(options) {
//         super(options);
//     }
//
//
//
//     /**
//      * Create a new widget given a context.
//      * @param context DocumentRegistry.IContext<DocumentRegistry.IModel>
//      * @return DocumentWidget
//      */
//     createNewWidget(context) {
//         // return new FitsViewerDocument(context);
//         return new DocumentWidget({ content:new FitsViewerWidget(context), context, reveal:true, toolbar:null });
//     }
// }
// const a= {
//     name: 'some-name',
//     fileTypes: ['csv'],
//     defaultFor: [],
//     defaultRendered: [],
//     readOnly: false,
//     modelName: 'text',
//     preferKernel: false,
//     canStartKernel: false,
//     widgetCreated: new Signal(null),
// }


/***/ }),

/***/ "./lib/SlateCommandExt.js":
/*!********************************!*\
  !*** ./lib/SlateCommandExt.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SlateRootWidget: () => (/* binding */ SlateRootWidget),
/* harmony export */   activateSlateCommandExt: () => (/* binding */ activateSlateCommandExt)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./FireflyCommonUtils.js */ "./lib/FireflyCommonUtils.js");





let widgetId;
let widgetCnt = 1;
let openWidgets = {};
/**
 * Extension can be started in two ways.
 * 1. as a jupyter command
 * 2. firefly_client sending a 'StartLabWindow' action
 * @param {JupyterFrontEnd} app
 * @param {ICommandPalette} palette
 * @param {ILauncher | null} launcher
 */
function activateSlateCommandExt(app, palette, launcher) {
    (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.findFirefly)().then((ffConfig) => {
        const { firefly } = ffConfig;
        firefly.util.addActionListener(['StartLabWindow'], (action, state) => {
            openSlateMulti(app, action.payload.renderTreeId, false);
        });
        firefly.util.addActionListener(['StartBrowserTab'], (action, state) => {
            firefly.setViewerConfig(firefly.ViewerType.Grid);
            firefly.getViewer(action.payload.channel).openViewer();
        });
    });
    // for starting extension as a jupyter command -----------
    const command = 'firefly:open-slate';
    const category = 'Firefly';
    app.commands.addCommand(command, {
        label: 'Open Firefly',
        caption: 'Open Firefly',
        isEnabled: () => true,
        execute: () => {
            const id = 'slate-' + widgetCnt;
            widgetCnt++;
            openSlateMulti(app, id, true);
        }
    });
    palette.addItem({ command, category });
    if (launcher)
        launcher.add({ command, category });
}
function openSlateMulti(app, id, activate) {
    activate = window.document.getElementById(id) || activate;
    if (!openWidgets[id]) {
        let widget = new SlateRootWidget(id);
        if (app.shell.addToMainArea)
            app.shell.addToMainArea(widget); // --- pre version 1
        else if (app.shell.add)
            app.shell.add(widget, 'main'); // version 1
        else
            throw Error('Could not add firefly to tab');
        (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.findFirefly)().then((ffConfig) => {
            const { action } = ffConfig.firefly;
            action.dispatchChangeActivePlotView(undefined);
        });
        openWidgets[id] = widget;
    }
    if (activate)
        app.shell.activateById(id);
}
/**
 * Open only one slate tab.  Using this funtion keeps the slate tab as a singleton.
 *
 * Currently not used.
 * @param app
 */
function openSlateSingleOnly(app) {
    if (!widgetId) {
        let widget = new SlateRootWidget('slate-1');
        app.shell.addToMainArea(widget);
        widgetId = widget.id;
        (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.findFirefly)().then((ffConfig) => {
            const { action } = ffConfig.firefly;
            action.dispatchChangeActivePlotView(undefined);
        });
    }
    else {
    }
    app.shell.activateById(widgetId);
}
class SlateRootWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Construct a new output widget.
     */
    constructor(id) {
        super({ node: createNode(id) });
        this.id = id;
        this.title.label = 'Firefly: ' + id;
        this.title.closable = true;
        (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.findFirefly)().then((ffConfig) => {
            this.startViewer(ffConfig.firefly, id);
        });
    }
    startViewer(firefly, id) {
        const { util, action } = firefly;
        const props = {
            div: id,
            renderTreeId: id,
            template: 'FireflySlate',
            disableDefaultDropDown: true,
        };
        const fallbackMenu = [
            { label: 'Images', action: 'ImageSelectDropDownSlateCmd' },
            { label: 'TAP Searches', action: 'TAPSearch' },
            { label: 'Catalogs', action: 'IrsaCatalogDropDown' },
            { label: 'Charts', action: 'ChartSelectDropDownCmd' },
            { label: 'Upload', action: 'FileUploadDropDownCmd' },
        ];
        if (!firefly.originalAppProps) {
            props.menu = fallbackMenu;
        }
        action.dispatchApiToolsView(true, false);
        this.controlApp = util.startAsAppFromApi(id, props);
    }
    dispose() {
        widgetId = undefined;
    }
    close() {
        super.close();
        widgetId = undefined;
        delete openWidgets[this.id];
        if (this.controlApp)
            this.controlApp.unrender();
        this.controlApp = undefined;
    }
    activate() {
        super.activate();
        if (this.controlApp) {
            this.controlApp.unrender();
            this.controlApp.render();
        }
        (0,_FireflyCommonUtils_js__WEBPACK_IMPORTED_MODULE_4__.findFirefly)().then((ffConfig) => {
            const { action } = ffConfig.firefly;
            action.dispatchChangeActivePlotView(undefined);
        });
    }
}
function createNode(filename) {
    const node = document.createElement('div');
    node.id = filename;
    const tmpElement = document.createElement('div');
    tmpElement.innerHTML = '<div>Firefly Loading...</div>';
    node.appendChild(tmpElement);
    return node;
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
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _SlateCommandExt_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./SlateCommandExt.js */ "./lib/SlateCommandExt.js");
/* harmony import */ var _FitsViewerExt_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./FitsViewerExt.js */ "./lib/FitsViewerExt.js");





/**
 * Initialization data for each extension.
 */
const showSlateExt = {
    id: 'jupyter_firefly_extensions:showSlate',
    description: 'Show firefly slate',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher],
    activate: _SlateCommandExt_js__WEBPACK_IMPORTED_MODULE_3__.activateSlateCommandExt
};
const fitsViewerExt = {
    id: 'jupyter_firefly_extensions:fitsviewer',
    description: 'View a FITS file',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: _FitsViewerExt_js__WEBPACK_IMPORTED_MODULE_4__.activateFitsViewerExt
};
// More than one extension/plugin can be exported as a list
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([showSlateExt, fitsViewerExt]);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.37ed69ecb7fce3ebc64a.js.map