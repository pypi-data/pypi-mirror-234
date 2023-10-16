(self["webpackChunkjupyterlab_broccoli_blocks"] = self["webpackChunkjupyterlab_broccoli_blocks"] || []).push([["lib_index_js"],{

/***/ "./lib/msg lazy recursive ^\\.\\/.*\\.js$":
/*!*****************************************************!*\
  !*** ./lib/msg/ lazy ^\.\/.*\.js$ namespace object ***!
  \*****************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var map = {
	"./En.js": [
		"./lib/msg/En.js",
		"lib_msg_En_js"
	],
	"./Jp.js": [
		"./lib/msg/Jp.js",
		"lib_msg_Jp_js"
	]
};
function webpackAsyncContext(req) {
	if(!__webpack_require__.o(map, req)) {
		return Promise.resolve().then(() => {
			var e = new Error("Cannot find module '" + req + "'");
			e.code = 'MODULE_NOT_FOUND';
			throw e;
		});
	}

	var ids = map[req], id = ids[0];
	return __webpack_require__.e(ids[1]).then(() => {
		return __webpack_require__(id);
	});
}
webpackAsyncContext.keys = () => (Object.keys(map));
webpackAsyncContext.id = "./lib/msg lazy recursive ^\\.\\/.*\\.js$";
module.exports = webpackAsyncContext;

/***/ }),

/***/ "./lib/blocks.js":
/*!***********************!*\
  !*** ./lib/blocks.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TOOLBOX: () => (/* binding */ TOOLBOX)
/* harmony export */ });
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly */ "webpack/sharing/consume/default/blockly/blockly");
/* harmony import */ var blockly__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _toolbox_basic__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./toolbox_basic */ "./lib/toolbox_basic.js");
/* harmony import */ var _toolbox_junkbox__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toolbox_junkbox */ "./lib/toolbox_junkbox.js");




//
const toolboxUtils = new _utils__WEBPACK_IMPORTED_MODULE_1__.ToolboxUtils();
const TOOLBOX = toolboxUtils.add(_toolbox_junkbox__WEBPACK_IMPORTED_MODULE_2__.TOOLBOX_JUNKBOX, _toolbox_basic__WEBPACK_IMPORTED_MODULE_3__.TOOLBOX_BASIC, 2);
// text_nocrlf_print
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'text_nocrlf_print',
        'message0': '%{BKY_BLOCK_TEXT_NOCRLF_PRINT}  %1',
        'args0': [
            {
                'type': 'input_value',
                'name': 'TEXT',
                'check': 'String',
            }
        ],
        'inputsInline': false,
        'previousStatement': null,
        'nextStatement': null,
        'colour': 230,
        'tooltip': '',
        'helpUrl': ''
    }]);
// color_hsv2rgb
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'color_hsv2rgb',
        'message0': '%{BKY_BLOCK_COLOR_HSV}  %1 %{BKY_BLOCK_COLOR_S}  %2 %{BKY_BLOCK_COLOR_V}  %3',
        'args0': [
            {
                'type': 'input_value',
                'name': 'H',
                'check': 'Number',
                'align': 'RIGHT'
            },
            {
                'type': 'input_value',
                'name': 'S',
                'check': 'Number',
                'align': 'RIGHT'
            },
            {
                'type': 'input_value',
                'name': 'V',
                'check': 'Number',
                'align': 'RIGHT'
            },
        ],
        'output': 'Colour',
        'colour': 230,
        'helpUrl': '',
        'tooltip': '',
    }]);


/***/ }),

/***/ "./lib/dart/func.js":
/*!**************************!*\
  !*** ./lib/dart/func.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   dummy_function: () => (/* binding */ dummy_function)
/* harmony export */ });
//import { dartGenerator as BlocklyGene } from 'blockly/dart';
const notImplementedMsg = 'Not implemented';
function dummy_function(block, generator) {
    return notImplementedMsg;
}
;


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var jupyterlab_broccoli__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jupyterlab-broccoli */ "webpack/sharing/consume/default/jupyterlab-broccoli/jupyterlab-broccoli");
/* harmony import */ var jupyterlab_broccoli__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jupyterlab_broccoli__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _blocks__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./blocks */ "./lib/blocks.js");
/* harmony import */ var _python_func_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./python/func.js */ "./lib/python/func.js");
/* harmony import */ var _javascript_func_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./javascript/func.js */ "./lib/javascript/func.js");
/* harmony import */ var _lua_func_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./lua/func.js */ "./lib/lua/func.js");
/* harmony import */ var _dart_func_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./dart/func.js */ "./lib/dart/func.js");
/* harmony import */ var _php_func_js__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./php/func.js */ "./lib/php/func.js");








/**
 * Initialization data for the jupyterlab-broccoli-blocks extension.
 */
const plugin = {
    id: 'jupyterlab-broccoli-blocks:plugin',
    autoStart: true,
    requires: [jupyterlab_broccoli__WEBPACK_IMPORTED_MODULE_0__.IBlocklyRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.ITranslator],
    activate: (app, register, translator) => {
        console.log('JupyterLab extension jupyterlab-broccoli-blocks is activated!');
        // Localization 
        const language = register.language;
        __webpack_require__("./lib/msg lazy recursive ^\\.\\/.*\\.js$")(`./${language}.js`)
            .catch(() => {
            if (language !== 'En') {
                __webpack_require__.e(/*! import() */ "lib_msg_En_js").then(__webpack_require__.bind(__webpack_require__, /*! ./msg/En.js */ "./lib/msg/En.js"))
                    .catch(() => { });
            }
        });
        const trans = (translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator).load('jupyterlab');
        register.registerToolbox(trans.__('Junk Box'), _blocks__WEBPACK_IMPORTED_MODULE_2__.TOOLBOX);
        //
        register.registerCodes('python', _python_func_js__WEBPACK_IMPORTED_MODULE_3__);
        register.registerCodes('javascript', _javascript_func_js__WEBPACK_IMPORTED_MODULE_4__);
        register.registerCodes('lua', _lua_func_js__WEBPACK_IMPORTED_MODULE_5__);
        register.registerCodes('dart', _dart_func_js__WEBPACK_IMPORTED_MODULE_6__);
        register.registerCodes('php', _php_func_js__WEBPACK_IMPORTED_MODULE_7__);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/javascript/func.js":
/*!********************************!*\
  !*** ./lib/javascript/func.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   text_nocrlf_print: () => (/* binding */ text_nocrlf_print),
/* harmony export */   text_print: () => (/* binding */ text_print)
/* harmony export */ });
/* harmony import */ var blockly_javascript__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly/javascript */ "./node_modules/blockly/javascript.js");
/* harmony import */ var blockly_javascript__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly_javascript__WEBPACK_IMPORTED_MODULE_0__);

const Order = {
    ATOMIC: 0,
    NEW: 1.1,
    MEMBER: 1.2,
    FUNCTION_CALL: 2,
    INCREMENT: 3,
    DECREMENT: 3,
    BITWISE_NOT: 4.1,
    UNARY_PLUS: 4.2,
    UNARY_NEGATION: 4.3,
    LOGICAL_NOT: 4.4,
    TYPEOF: 4.5,
    VOID: 4.6,
    DELETE: 4.7,
    AWAIT: 4.8,
    EXPONENTIATION: 5.0,
    MULTIPLICATION: 5.1,
    DIVISION: 5.2,
    MODULUS: 5.3,
    SUBTRACTION: 6.1,
    ADDITION: 6.2,
    BITWISE_SHIFT: 7,
    RELATIONAL: 8,
    IN: 8,
    INSTANCEOF: 8,
    EQUALITY: 9,
    BITWISE_AND: 10,
    BITWISE_XOR: 11,
    BITWISE_OR: 12,
    LOGICAL_AND: 13,
    LOGICAL_OR: 14,
    CONDITIONAL: 15,
    ASSIGNMENT: 16,
    YIELD: 17,
    COMMA: 18,
    NONE: 99, // (...)
};
const notImplementedMsg = 'Not implemented at this Kernel';
function text_print(block) {
    const msg = blockly_javascript__WEBPACK_IMPORTED_MODULE_0__.javascriptGenerator.valueToCode(block, 'TEXT', Order.NONE) || "''";
    return 'console.log(' + msg + ');\n';
}
;
function text_nocrlf_print(block) {
    const msg = blockly_javascript__WEBPACK_IMPORTED_MODULE_0__.javascriptGenerator.valueToCode(block, 'TEXT', Order.NONE) || "''";
    return 'process.stdout.write(' + msg + ');\n';
}
;


/***/ }),

/***/ "./lib/lua/func.js":
/*!*************************!*\
  !*** ./lib/lua/func.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   dummy_function: () => (/* binding */ dummy_function)
/* harmony export */ });
//import { luaGenerator as BlocklyGene } from 'blockly/lua';
const notImplementedMsg = 'Not implemented';
function dummy_function(block, generator) {
    return notImplementedMsg;
}
;


/***/ }),

/***/ "./lib/php/func.js":
/*!*************************!*\
  !*** ./lib/php/func.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   dummy_function: () => (/* binding */ dummy_function)
/* harmony export */ });
//import { phpGenerator as BlocklyGene } from 'blockly/php';
const notImplementedMsg = 'Not implemented';
function dummy_function(block, generator) {
    return notImplementedMsg;
}
;


/***/ }),

/***/ "./lib/python/func.js":
/*!****************************!*\
  !*** ./lib/python/func.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   color_hsv2rgb: () => (/* binding */ color_hsv2rgb),
/* harmony export */   text_nocrlf_print: () => (/* binding */ text_nocrlf_print)
/* harmony export */ });
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! blockly/python */ "./node_modules/blockly/python.js");
/* harmony import */ var blockly_python__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(blockly_python__WEBPACK_IMPORTED_MODULE_0__);

const Order = {
    ATOMIC: 0,
    COLLECTION: 1,
    STRING_CONVERSION: 1,
    MEMBER: 2.1,
    FUNCTION_CALL: 2.2,
    EXPONENTIATION: 3,
    UNARY_SIGN: 4,
    BITWISE_NOT: 4,
    MULTIPLICATIVE: 5,
    ADDITIVE: 6,
    BITWISE_SHIFT: 7,
    BITWISE_AND: 8,
    BITWISE_XOR: 9,
    BITWISE_OR: 10,
    RELATIONAL: 11,
    LOGICAL_NOT: 12,
    LOGICAL_AND: 13,
    LOGICAL_OR: 14,
    CONDITIONAL: 15,
    LAMBDA: 16,
    NONE: 99, // (...)
};
/**/
//
//const notImplementedMsg = 'Not implemented at this Kernel';
function text_nocrlf_print(block) {
    const msg = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'TEXT', Order.NONE) || "''";
    return 'print(' + msg + ', end="")\n';
}
;
//
function color_hsv2rgb(block) {
    let hh = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'H', Order.NONE) || "''";
    let ss = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'S', Order.NONE) || "''";
    let vv = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'V', Order.NONE) || "''";
    hh = hh % 360;
    if (hh < 0.0)
        hh = hh + 360;
    if (ss < 0.0)
        ss = 0.0;
    else if (ss > 1.0)
        ss = 1.0;
    if (vv < 0.0)
        vv = 0.0;
    else if (vv > 1.0)
        vv = 1.0;
    let aa = vv;
    let bb = vv - vv * ss;
    let rc = 0;
    let gc = 0;
    let bc = 0;
    //
    if (hh >= 0 && hh < 60) {
        rc = aa;
        gc = (hh / 60) * (aa - bb) + bb;
        bc = bb;
    }
    else if (hh >= 60 && hh < 120) {
        rc = (120 - hh) / 60 * (aa - bb) + bb;
        gc = aa;
        bc = bb;
    }
    else if (hh >= 120 && hh < 180) {
        rc = bb;
        gc = aa;
        bc = (hh - 120) / 60 * (aa - bb) + bb;
    }
    else if (hh >= 180 && hh < 240) {
        rc = bb;
        gc = (240 - hh) / 60 * (aa - bb) + bb;
        bc = aa;
    }
    else if (hh >= 240 && hh < 300) {
        rc = (hh - 240) / 60 * (aa - bb) + bb;
        gc = bb;
        bc = aa;
    }
    else { // hh>=300 and hh<360
        rc = aa;
        gc = bb;
        bc = (360 - hh) / 50 * (aa - bb) + bb;
    }
    //
    rc = Math.trunc(rc * 255);
    gc = Math.trunc(gc * 255);
    bc = Math.trunc(bc * 255);
    //
    const rgb = '#' + rc.toString(16) + gc.toString(16) + bc.toString(16);
    const code = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.quote_(rgb);
    return [code, Order.FUNCTION_CALL];
}
;
/**/


/***/ }),

/***/ "./lib/toolbox_basic.js":
/*!******************************!*\
  !*** ./lib/toolbox_basic.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TOOLBOX_BASIC: () => (/* binding */ TOOLBOX_BASIC)
/* harmony export */ });
//
const TOOLBOX_BASIC = {
    kind: 'categoryToolbox',
    contents: [
        {
            kind: 'category',
            name: '%{BKY_TOOLBOX_LOGIC}',
            colour: '210',
            contents: [
                {
                    kind: 'block',
                    type: 'controls_if'
                },
                {
                    kind: 'BLOCK',
                    type: 'logic_compare'
                },
                {
                    kind: 'BLOCK',
                    type: 'logic_operation',
                    blockxml: `<block type='logic_operation'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'logic_negate',
                    blockxml: `<block type='logic_negate'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'logic_boolean',
                    blockxml: `<block type='logic_boolean'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'logic_null',
                    blockxml: `<block type='logic_null'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'logic_ternary',
                    blockxml: `<block type='logic_ternary'></block>`
                }
            ]
        },
        {
            kind: 'category',
            name: '%{BKY_TOOLBOX_LOOPS}',
            colour: '120',
            contents: [
                {
                    kind: 'BLOCK',
                    type: 'controls_repeat_ext',
                    blockxml: `<block type='controls_repeat_ext'>
               <value name='TIMES'>
                 <shadow type='math_number'>
                   <field name='NUM'>10</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'controls_whileUntil',
                    blockxml: `<block type='controls_whileUntil'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'controls_for',
                    blockxml: `<block type='controls_for'>
               <value name='FROM'>
                 <shadow type='math_number'>
                   <field name='NUM'>1</field>
                 </shadow>
               </value>
               <value name='TO'>
                 <shadow type='math_number'>
                   <field name='NUM'>10</field>
                 </shadow>
               </value>
               <value name='BY'>
                 <shadow type='math_number'>
                   <field name='NUM'>1</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'controls_forEach',
                    blockxml: `<block type='controls_forEach'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'controls_flow_statements',
                    blockxml: `<block type='controls_flow_statements'></block>`
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_MATH}',
            colour: '230',
            contents: [
                {
                    kind: 'BLOCK',
                    type: 'math_number',
                    blockxml: `<block type='math_number'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_arithmetic',
                    blockxml: `<block type='math_arithmetic'>
               <value name='A'>
                 <shadow type='math_number'>
                   <field name='NUM'>1</field>
                 </shadow>
               </value>
               <value name='B'>
                 <shadow type='math_number'>
                   <field name='NUM'>1</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_single',
                    blockxml: `<block type='math_single'>
               <value name='NUM'>
                 <shadow type='math_number'>
                   <field name='NUM'>9</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_trig',
                    blockxml: `<block type='math_trig'>
               <value name='NUM'>
                 <shadow type='math_number'>
                   <field name='NUM'>45</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_constant',
                    blockxml: `<block type='math_constant'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_number_property',
                    blockxml: `<block type='math_number_property'>
               <value name='NUMBER_TO_CHECK'>
                 <shadow type='math_number'>
                   <field name='NUM'>0</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_change',
                    blockxml: `<block type='math_change'>
               <value name='DELTA'>
                 <shadow type='math_number'>
                   <field name='NUM'>1</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_round',
                    blockxml: `<block type='math_round'>
               <value name='NUM'>
                 <shadow type='math_number'>
                   <field name='NUM'>3.1</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_on_list',
                    blockxml: `<block type='math_on_list'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_modulo',
                    blockxml: `<block type='math_modulo'>
               <value name='DIVIDEND'>
                 <shadow type='math_number'>
                   <field name='NUM'>64</field>
                 </shadow>
               </value>
               <value name='DIVISOR'>
                 <shadow type='math_number'>
                   <field name='NUM'>10</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_constrain',
                    blockxml: `<block type='math_constrain'>
              <value name='VALUE'>
                <shadow type='math_number'>
                  <field name='NUM'>50</field>
                </shadow>
              </value>
              <value name='LOW'>
                <shadow type='math_number'>
                  <field name='NUM'>1</field>
                </shadow>
              </value>
              <value name='HIGH'>
                <shadow type='math_number'>
                  <field name='NUM'>100</field>
                </shadow>
              </value>
            </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_random_int',
                    blockxml: `<block type='math_random_int'>
               <value name='FROM'>
                 <shadow type='math_number'>
                   <field name='NUM'>1</field>
                 </shadow>
               </value>
               <value name='TO'>
                 <shadow type='math_number'>
                   <field name='NUM'>100</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'math_random_float',
                    blockxml: `<block type='math_random_float'></block>`
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_TEXT}',
            colour: '160',
            contents: [
                {
                    kind: 'BLOCK',
                    type: 'text',
                    blockxml: `<block type='text'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_join',
                    blockxml: `<block type='text_join'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_append',
                    blockxml: `<block type='text_append'>
               <value name='TEXT'>
                 <shadow type='text'></shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_length',
                    blockxml: `<block type='text_length'>
               <value name='VALUE'>
                 <shadow type='text'>
                   <field name='TEXT'>abc</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_isEmpty',
                    blockxml: `<block type='text_isEmpty'>
               <value name='VALUE'>
                 <shadow type='text'>
                   <field name='TEXT'></field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_indexOf',
                    blockxml: `<block type='text_indexOf'>
               <value name='VALUE'>
                 <block type='variables_get'>
                   <field name='VAR'>text</field>
                 </block>
               </value>
               <value name='FIND'>
                 <shadow type='text'>
                   <field name='TEXT'>abc</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_charAt',
                    blockxml: `<block type='text_charAt'>
               <value name='VALUE'>
                 <block type='variables_get'>
                   <field name='VAR'>text</field>
                 </block>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_getSubstring',
                    blockxml: `<block type='text_getSubstring'>
               <value name='STRING'>
                 <block type='variables_get'>
                   <field name='VAR'>text</field>
                 </block>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_changeCase',
                    blockxml: `<block type='text_changeCase'>
               <value name='TEXT'>
                 <shadow type='text'>
                   <field name='TEXT'>abc</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_trim',
                    blockxml: `<block type='text_trim'>
               <value name='TEXT'>
                 <shadow type='text'>
                   <field name='TEXT'>abc</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_print',
                    blockxml: `<block type='text_print'>
               <value name='TEXT'>
                 <shadow type='text'>
                   <field name='TEXT'>abc</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'text_prompt_ext',
                    blockxml: `<block type='text_prompt_ext'>
               <value name='TEXT'>
                 <shadow type='text'>
                   <field name='TEXT'>abc</field>
                 </shadow>
               </value>
             </block>`
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_LISTS}',
            colour: '260',
            contents: [
                {
                    kind: 'BLOCK',
                    type: 'lists_create_with',
                    blockxml: `<block type='lists_create_with'>
               <mutation items='0'></mutation>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'lists_create_with',
                    blockxml: `<block type='lists_create_with'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'lists_repeat',
                    blockxml: `<block type='lists_repeat'>
               <value name='NUM'>
                 <shadow type='math_number'>
                   <field name='NUM'>5</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'lists_length',
                    blockxml: `<block type='lists_length'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'lists_isEmpty',
                    blockxml: `<block type='lists_isEmpty'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'lists_indexOf',
                    blockxml: `<block type='lists_indexOf'>
               <value name='VALUE'>
                 <block type='variables_get'>
                   <field name='VAR'>list</field>
                 </block>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'lists_getIndex',
                    blockxml: `<block type='lists_getIndex'>
               <value name='VALUE'>
                 <block type='variables_get'>
                   <field name='VAR'>list</field>
                 </block>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'lists_setIndex',
                    blockxml: `<block type='lists_setIndex'>
               <value name='LIST'>
                 <block type='variables_get'>
                   <field name='VAR'>list</field>
                 </block>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'lists_getSublist',
                    blockxml: `<block type='lists_getSublist'>
               <value name='LIST'>
                 <block type='variables_get'>
                   <field name='VAR'>list</field>
                 </block>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'lists_split',
                    blockxml: `<block type='lists_split'>
               <value name='DELIM'>
                 <shadow type='text'>
                   <field name='TEXT'>,</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'lists_sort',
                    blockxml: `<block type='lists_sort'></block>`
                }
            ]
        },
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_COLOR}',
            colour: '20',
            contents: [
                {
                    kind: 'BLOCK',
                    type: 'colour_picker',
                    blockxml: `<block type='colour_picker'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'colour_random',
                    blockxml: `<block type='colour_random'></block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'colour_rgb',
                    blockxml: `<block type='colour_rgb'>
               <value name='RED'>
                 <shadow type='math_number'>
                   <field name='NUM'>100</field>
                 </shadow>
               </value>
               <value name='GREEN'>
                 <shadow type='math_number'>
                   <field name='NUM'>50</field>
                 </shadow>
               </value>
               <value name='BLUE'>
                 <shadow type='math_number'>
                   <field name='NUM'>0</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'colour_blend',
                    blockxml: `<block type='colour_blend'>
               <value name='COLOUR1'>
                 <shadow type='colour_picker'>
                   <field name='COLOUR'>#ff0000</field>
                 </shadow>
               </value>
             <value name='COLOUR2'>
               <shadow type='colour_picker'>
                 <field name='COLOUR'>#3333ff</field>
               </shadow>
             </value>
             <value name='RATIO'>
               <shadow type='math_number'>
                 <field name='NUM'>0.5</field>
               </shadow>
             </value>
           </block>`
                }
            ]
        },
        {
            kind: 'SEP'
        },
        {
            kind: 'CATEGORY',
            custom: 'VARIABLE',
            colour: '330',
            name: '%{BKY_TOOLBOX_VARIABLES}'
        },
        {
            kind: 'CATEGORY',
            custom: 'PROCEDURE',
            colour: '290',
            name: '%{BKY_TOOLBOX_FUNCTIONS}'
        },
    ]
};


/***/ }),

/***/ "./lib/toolbox_junkbox.js":
/*!********************************!*\
  !*** ./lib/toolbox_junkbox.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TOOLBOX_JUNKBOX: () => (/* binding */ TOOLBOX_JUNKBOX)
/* harmony export */ });
const TOOLBOX_JUNKBOX = {
    kind: 'categoryToolbox',
    contents: [
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_JUNKBOX}',
            colour: 330,
            contents: [
                {
                    kind: 'BLOCK',
                    type: 'text_nocrlf_print',
                    blockxml: `<block type='text_nocrlf_print'>
              <value name='TEXT'>
                <shadow type='text'>
                  <field name='TEXT'>abc</field>
                </shadow>
              </value>
            </block>`,
                },
                {
                    kind: 'BLOCK',
                    type: 'color_hsv2rgb',
                    blockxml: `<block type='color_hsv2rgb'>
              <value name='H'>
                <shadow type='math_number'>
                  <field name='NUM'>0.0</field>
                </shadow>
              </value>
              <value name='S'>
                <shadow type='math_number'>
                  <field name='NUM'>0.45</field>
                </shadow>
              </value>
              <value name='V'>
                <shadow type='math_number'>
                  <field name='NUM'>0.65</field>
                </shadow>
              </value>
            </block>`,
                },
            ]
        }
    ]
};


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ToolboxUtils: () => (/* binding */ ToolboxUtils)
/* harmony export */ });
//
class ToolboxUtils {
    constructor() { }
    add(a, b, num) {
        //
        if (a.kind !== b.kind)
            undefined;
        const c = { kind: a.kind, contents: new Array };
        const a_len = a.contents.length;
        const b_len = b.contents.length;
        for (let i = 0; i < a_len; i++) {
            c.contents[i] = a.contents[i];
        }
        // separator
        for (let i = 0; i < num; i++) {
            c.contents[a_len + i] = { kind: 'SEP' };
        }
        for (let i = 0; i < b_len; i++) {
            c.contents[a_len + num + i] = b.contents[i];
        }
        return c;
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.77a5bc6511332221d43e.js.map