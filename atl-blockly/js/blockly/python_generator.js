/**
 * @license
 * Visual Blocks Language
 *
 * Copyright 2012 Google Inc.
 * https://developers.google.com/blockly/
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * @fileoverview Generating Python for thymio blocks.
 * @author AutreTechLab
 */
'use strict';

goog.provide('Blockly.Python.atl');

goog.require('Blockly.Python');


Blockly.Python['atl_comment'] = function(block) {
  var value_atl_comment_in_code_text = Blockly.Python.valueToCode(block, 'ATL_COMMENT_IN_CODE_TEXT', Blockly.Python.ORDER_ATOMIC);
  // TODO: Assemble Python into code variable.
  var code = '#' + value_atl_comment_in_code_text;
  return code;
};