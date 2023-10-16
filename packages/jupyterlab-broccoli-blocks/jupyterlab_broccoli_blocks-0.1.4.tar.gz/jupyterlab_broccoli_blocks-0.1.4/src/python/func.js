
import { pythonGenerator as BlocklyGene } from 'blockly/python';

const Order = {
  ATOMIC: 0,             // 0 "" ...
  COLLECTION: 1,         // tuples, lists, dictionaries
  STRING_CONVERSION: 1,  // `expression...`
  MEMBER: 2.1,           // . []
  FUNCTION_CALL: 2.2,    // ()
  EXPONENTIATION: 3,     // **
  UNARY_SIGN: 4,         // + -
  BITWISE_NOT: 4,        // ~
  MULTIPLICATIVE: 5,     // * / // %
  ADDITIVE: 6,           // + -
  BITWISE_SHIFT: 7,      // << >>
  BITWISE_AND: 8,        // &
  BITWISE_XOR: 9,        // ^
  BITWISE_OR: 10,        // |
  RELATIONAL: 11,        // in, not in, is, is not, >, >=, <>, !=, ==
  LOGICAL_NOT: 12,       // not
  LOGICAL_AND: 13,       // and
  LOGICAL_OR: 14,        // or
  CONDITIONAL: 15,       // if else
  LAMBDA: 16,            // lambda
  NONE: 99,              // (...)
};
/**/

//
//const notImplementedMsg = 'Not implemented at this Kernel';

export function text_nocrlf_print(block) {
  const msg = BlocklyGene.valueToCode(block, 'TEXT', Order.NONE) || "''";
  return 'print(' + msg + ', end="")\n';
};

//
export function color_hsv2rgb(block) {
  let hh = BlocklyGene.valueToCode(block, 'H', Order.NONE) || "''";
  let ss = BlocklyGene.valueToCode(block, 'S', Order.NONE) || "''";
  let vv = BlocklyGene.valueToCode(block, 'V', Order.NONE) || "''";

  hh = hh % 360;
  if (hh<0.0) hh = hh + 360;
  if (ss<0.0) ss = 0.0
  else if (ss>1.0) ss = 1.0;
  if (vv<0.0) vv = 0.0
  else if (vv>1.0) vv = 1.0;

  let aa = vv;
  let bb = vv - vv*ss;
  let rc = 0;
  let gc = 0;
  let bc = 0;
  //
  if (hh>=0 && hh<60) {
    rc = aa;
    gc = (hh/60)*(aa - bb) + bb;
    bc = bb;
  }
  else if (hh>=60 && hh<120) {
    rc = (120 - hh)/60*(aa - bb) + bb;
    gc = aa;
    bc = bb;
  }
  else if (hh>=120 && hh<180) {
    rc = bb;
    gc = aa;
    bc = (hh - 120)/60*(aa - bb) + bb;
  }
  else if (hh>=180 && hh<240) {
    rc = bb;
    gc = (240 - hh)/60*(aa - bb) + bb;
    bc = aa;
  }
  else if (hh>=240 && hh<300) {
    rc = (hh - 240)/60*(aa - bb) + bb;
    gc = bb;
    bc = aa;
  }
  else {           // hh>=300 and hh<360
    rc = aa;
    gc = bb;
    bc = (360 - hh)/50*(aa - bb) + bb;
  }
  //
  rc = Math.trunc(rc*255);
  gc = Math.trunc(gc*255);
  bc = Math.trunc(bc*255);
  //
  const rgb = '#' + rc.toString(16) + gc.toString(16) + bc.toString(16);
  const code = BlocklyGene.quote_(rgb);
  return [code, Order.FUNCTION_CALL];
};
/**/

