(self["webpackChunkjupyterlab_broccoli_turtle"] = self["webpackChunkjupyterlab_broccoli_turtle"] || []).push([["lib_index_js"],{

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
/* harmony import */ var _toolbox_turtle__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toolbox_turtle */ "./lib/toolbox_turtle.js");




//
const toolboxUtils = new _utils__WEBPACK_IMPORTED_MODULE_1__.ToolboxUtils();
const TOOLBOX = toolboxUtils.add(_toolbox_turtle__WEBPACK_IMPORTED_MODULE_2__.TOOLBOX_TURTLE, _toolbox_basic__WEBPACK_IMPORTED_MODULE_3__.TOOLBOX_BASIC, 2);
// Init
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_init',
        'message0': '%{BKY_BLOCK_TURTLE_INIT}  %1 %{BKY_BLOCK_TURTLE_XSIZE}  %2 %{BKY_BLOCK_TURTLE_YSIZE}  %3',
        'args0': [
            {
                'type': 'input_dummy'
            },
            {
                'type': 'input_value',
                'name': 'XSIZE',
                'check': 'Number',
                'align': 'RIGHT'
            },
            {
                'type': 'input_value',
                'name': 'YSIZE',
                'check': 'Number',
                'align': 'RIGHT'
            }
        ],
        'nextStatement': null,
        'colour': 5,
        'tooltip': '',
        'helpUrl': ''
    }]);
// Turtle Speed
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_speed',
        'message0': '%{BKY_BLOCK_TURTLE_SPEED}  %1',
        'args0': [
            {
                'type': 'input_value',
                'name': 'VAL',
                'check': 'Number'
            }
        ],
        'previousStatement': null,
        'nextStatement': null,
        'colour': 290,
        'tooltip': '',
        'helpUrl': ''
    }]);
// Line Width
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_line_width',
        'message0': '%{BKY_BLOCK_TURTLE_WIDTH}  %1',
        'args0': [
            {
                'type': 'input_value',
                'name': 'VAL',
                'check': 'Number'
            }
        ],
        'previousStatement': null,
        'nextStatement': null,
        'colour': 290,
        'tooltip': '',
        'helpUrl': ''
    }]);
// Line Color
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_line_color',
        'message0': '%{BKY_BLOCK_TURTLE_COLOR}  %1',
        'args0': [
            {
                'type': 'input_value',
                'name': 'VAL',
                'check': 'Colour'
            }
        ],
        'previousStatement': null,
        'nextStatement': null,
        'colour': 290,
        'tooltip': '',
        'helpUrl': ''
    }]);
// Line HSV Color
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_line_hsv',
        'message0': '%{BKY_BLOCK_TURTLE_HSV} %1' +
            '%{BKY_BLOCK_TURTLE_HSV_S}  %2' +
            '%{BKY_BLOCK_TURTLE_HSV_V}  %3',
        'args0': [
            {
                'type': 'input_value',
                'name': 'H',
                'check': 'Number',
                'align': 'RIGHT',
            },
            {
                'type': 'input_value',
                'name': 'S',
                'check': 'Number',
                'align': 'RIGHT',
            },
            {
                'type': 'input_value',
                'name': 'V',
                'check': 'Number',
                'align': 'RIGHT',
            },
        ],
        'previousStatement': null,
        'nextStatement': null,
        'colour': 290,
        'tooltip': '',
        'helpUrl': ''
    }]);
// Pen Up
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_pen_up',
        'message0': '%{BKY_BLOCK_TURTLE_PEN_UP}',
        'previousStatement': null,
        'nextStatement': null,
        'colour': 50,
        'tooltip': '',
        'helpUrl': ''
    }]);
// Pen Down
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_pen_down',
        'message0': '%{BKY_BLOCK_TURTLE_PEN_DOWN}',
        'previousStatement': null,
        'nextStatement': null,
        'colour': 50,
        'tooltip': '',
        'helpUrl': ''
    }]);
// Foward
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_forward',
        'message0': '%{BKY_BLOCK_TURTLE_FORWARD}  %1',
        'args0': [
            {
                'type': 'input_value',
                'name': 'VAL',
                'check': 'Number'
            }
        ],
        'previousStatement': null,
        'nextStatement': null,
        'colour': 200,
        'tooltip': '',
        'helpUrl': ''
    }]);
// Turn Right
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_turn_right',
        'message0': '%{BKY_BLOCK_TURTLE_TURN_RIGHT}  %1',
        'args0': [
            {
                'type': 'input_value',
                'name': 'VAL',
                'check': 'Number'
            }
        ],
        'previousStatement': null,
        'nextStatement': null,
        'colour': 200,
        'tooltip': '',
        'helpUrl': ''
    }]);
// Turn Left
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_turn_left',
        'message0': '%{BKY_BLOCK_TURTLE_TURN_LEFT}  %1',
        'args0': [
            {
                'type': 'input_value',
                'name': 'VAL',
                'check': 'Number'
            }
        ],
        'previousStatement': null,
        'nextStatement': null,
        'colour': 200,
        'tooltip': '',
        'helpUrl': ''
    }]);
// Move to
blockly__WEBPACK_IMPORTED_MODULE_0__.defineBlocksWithJsonArray([{
        'type': 'turtle_move',
        'message0': '%{BKY_BLOCK_TURTLE_MOVE}  %1 %{BKY_BLOCK_TURTLE_XPOS}  %2 %{BKY_BLOCK_TURTLE_YPOS}  %3',
        'args0': [
            {
                'type': 'input_dummy'
            },
            {
                'type': 'input_value',
                'name': 'XPOS',
                'check': 'Number',
                'align': 'RIGHT'
            },
            {
                'type': 'input_value',
                'name': 'YPOS',
                'check': 'Number',
                'align': 'RIGHT'
            }
        ],
        'previousStatement': null,
        'nextStatement': null,
        'colour': 200,
        'tooltip': '',
        'helpUrl': ''
    }]);


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





//import * as func_lua from './lua/func.js';
//import * as func_dart from './dart/func.js';
//import * as func_php from './php/func.js';
/**
 * Initialization data for the jupyterlab-broccoli-turtle extension.
 */
const plugin = {
    id: 'jupyterlab-broccoli-turtle:plugin',
    autoStart: true,
    requires: [jupyterlab_broccoli__WEBPACK_IMPORTED_MODULE_0__.IBlocklyRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.ITranslator],
    activate: (app, register, translator) => {
        console.log('JupyterLab extension jupyterlab-broccoli-turtle is activated!');
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
        register.registerToolbox(trans.__('Turtle'), _blocks__WEBPACK_IMPORTED_MODULE_2__.TOOLBOX);
        register.registerCodes('python', _python_func_js__WEBPACK_IMPORTED_MODULE_3__);
        register.registerCodes('javascript', _javascript_func_js__WEBPACK_IMPORTED_MODULE_4__);
        //register.registerCodes('lua', func_lua);
        //register.registerCodes('dart', func_dart);
        //register.registerCodes('php', func_php);
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
/* harmony export */   turtle_init: () => (/* binding */ turtle_init)
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
function turtle_init(block) {
    alert(notImplementedMsg);
    return 'console.log(' + notImplementedMsg + ');\n';
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
/* harmony export */   turtle_forward: () => (/* binding */ turtle_forward),
/* harmony export */   turtle_init: () => (/* binding */ turtle_init),
/* harmony export */   turtle_line_color: () => (/* binding */ turtle_line_color),
/* harmony export */   turtle_line_hsv: () => (/* binding */ turtle_line_hsv),
/* harmony export */   turtle_line_width: () => (/* binding */ turtle_line_width),
/* harmony export */   turtle_move: () => (/* binding */ turtle_move),
/* harmony export */   turtle_pen_down: () => (/* binding */ turtle_pen_down),
/* harmony export */   turtle_pen_up: () => (/* binding */ turtle_pen_up),
/* harmony export */   turtle_speed: () => (/* binding */ turtle_speed),
/* harmony export */   turtle_turn_left: () => (/* binding */ turtle_turn_left),
/* harmony export */   turtle_turn_right: () => (/* binding */ turtle_turn_right)
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
//
//const notImplementedMsg = 'Not implemented at this Kernel';
function turtle_init(block) {
    const xsz = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'XSIZE', Order.NONE) || "''";
    const ysz = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'YSIZE', Order.NONE) || "''";
    const msg = 'from jbturtle import *\n' +
        'from math import * \n\n' +
        'turtle = JBTurtle(' + xsz + ', ' + ysz + ')\n';
    return msg;
}
;
function turtle_speed(block) {
    const val = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'VAL', Order.NONE) || "''";
    return 'turtle.speed(' + val + ')\n';
}
;
function turtle_line_width(block) {
    const val = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'VAL', Order.NONE) || "''";
    return 'turtle.line_width(' + val + ')\n';
}
;
function turtle_line_color(block) {
    const val = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'VAL', Order.NONE) || "''";
    return 'turtle.line_color(' + val + ')\n';
}
;
function turtle_line_hsv(block) {
    const hh = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'H', Order.NONE) || "''";
    const ss = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'S', Order.NONE) || "''";
    const vv = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'V', Order.NONE) || "''";
    return 'turtle.line_hsv(' + hh + ', ' + ss + ', ' + vv + ')\n';
}
;
function turtle_pen_up(block) {
    return 'turtle.pen_up()\n';
}
;
function turtle_pen_down(block) {
    return 'turtle.pen_down()\n';
}
;
function turtle_forward(block) {
    const val = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'VAL', Order.NONE) || "''";
    return 'turtle.forward(' + val + ')\n';
}
;
function turtle_turn_right(block) {
    const val = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'VAL', Order.NONE) || "''";
    return 'turtle.turn_right(' + val + ')\n';
}
;
function turtle_turn_left(block) {
    const val = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'VAL', Order.NONE) || "''";
    return 'turtle.turn_left(' + val + ')\n';
}
;
function turtle_move(block) {
    const xp = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'XPOS', Order.NONE) || "''";
    const yp = blockly_python__WEBPACK_IMPORTED_MODULE_0__.pythonGenerator.valueToCode(block, 'YPOS', Order.NONE) || "''";
    return 'turtle.move(' + xp + ', ' + yp + ')\n';
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

/***/ "./lib/toolbox_turtle.js":
/*!*******************************!*\
  !*** ./lib/toolbox_turtle.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TOOLBOX_TURTLE: () => (/* binding */ TOOLBOX_TURTLE)
/* harmony export */ });
const TOOLBOX_TURTLE = {
    kind: 'categoryToolbox',
    contents: [
        {
            kind: 'CATEGORY',
            name: '%{BKY_TOOLBOX_TURTLE}',
            colour: '5',
            contents: [
                {
                    kind: 'BLOCK',
                    type: 'turtle_init',
                    blockxml: `<block type='turtle_init'>
               <value name='XSIZE'>
                 <shadow type='math_number'>
                   <field name='NUM'>640</field>
                 </shadow>
               </value>
               <value name='YSIZE'>
                 <shadow type='math_number'>
                   <field name='NUM'>400</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'turtle_speed',
                    blockxml: `<block type='turtle_speed'>
               <value name='VAL'>
                 <shadow type='math_number'>
                   <field name='NUM'>2</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'turtle_line_width',
                    blockxml: `<block type='turtle_line_width'>
               <value name='VAL'>
                 <shadow type='math_number'>
                   <field name='NUM'>2</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'turtle_line_color',
                    blockxml: `<block type='turtle_line_color'>
               <value name='VAL'>
                 <shadow type='colour_picker'>
                   <field name='COLOUR'>#000000</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'turtle_line_hsv',
                    blockxml: `<block type='turtle_line_hsv'>
               <value name='H'>
                 <shadow type='math_number'>
                   <field name='NUM'>0</field>
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
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'turtle_pen_down',
                },
                {
                    kind: 'BLOCK',
                    type: 'turtle_pen_up',
                },
                {
                    kind: 'BLOCK',
                    type: 'turtle_forward',
                    blockxml: `<block type='turtle_forward'>
               <value name='VAL'>
                 <shadow type='math_number'>
                   <field name='NUM'>100</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'turtle_turn_right',
                    blockxml: `<block type='turtle_turn_right'>
               <value name='VAL'>
                 <shadow type='math_number'>
                   <field name='NUM'>90</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'turtle_turn_left',
                    blockxml: `<block type='turtle_turn_left'>
               <value name='VAL'>
                 <shadow type='math_number'>
                   <field name='NUM'>90</field>
                 </shadow>
               </value>
             </block>`
                },
                {
                    kind: 'BLOCK',
                    type: 'turtle_move',
                    blockxml: `<block type='turtle_move'>
               <value name='XPOS'>
                 <shadow type='math_number'>
                   <field name='NUM'>0</field>
                 </shadow>
               </value>
               <value name='YPOS'>
                 <shadow type='math_number'>
                   <field name='NUM'>0</field>
                 </shadow>
               </value>
             </block>`
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
//# sourceMappingURL=lib_index_js.7a42fbc20e14c046a3be.js.map