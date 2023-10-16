
import * as Blockly from 'blockly';

import { ToolboxUtils } from './utils';
import { TOOLBOX_BASIC } from './toolbox_basic';
import { TOOLBOX_JUNKBOX } from './toolbox_junkbox';

//
const toolboxUtils = new ToolboxUtils();
export const TOOLBOX = toolboxUtils.add(TOOLBOX_JUNKBOX, TOOLBOX_BASIC, 2);

// text_nocrlf_print
Blockly.defineBlocksWithJsonArray(
[{
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
Blockly.defineBlocksWithJsonArray(
[{
  'type': 'color_hsv2rgb',
  'message0': 
    '%{BKY_BLOCK_COLOR_HSV}  %1 %{BKY_BLOCK_COLOR_S}  %2 %{BKY_BLOCK_COLOR_V}  %3',
  'args0': [
    {
      'type':  'input_value',
      'name':  'H',
      'check': 'Number',
      'align': 'RIGHT'
    },
    {
      'type':  'input_value',
      'name':  'S',
      'check': 'Number',
      'align': 'RIGHT'
    },
    {
      'type':  'input_value',
      'name':  'V',
      'check': 'Number',
      'align': 'RIGHT'
    },
  ],
  'output': 'Colour',
  'colour': 230,
  'helpUrl': '',
  'tooltip': '',
}]);

