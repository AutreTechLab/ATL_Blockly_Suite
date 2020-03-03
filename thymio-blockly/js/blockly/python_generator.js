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

goog.provide('Blockly.Python.thymio');

goog.require('Blockly.Python');


Blockly.Python['thymio_event_button'] = function(block) {
  var dropdown_button = block.getFieldValue('BUTTON');
  var dropdown_mode = block.getFieldValue('MODE');
  var statements_handler = Blockly.Python.statementToCode(block, 'HANDLER');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['thymio_event_prox'] = function(block) {
  var dropdown_sensor = block.getFieldValue('SENSOR');
  var dropdown_mode = block.getFieldValue('MODE');
  var statements_handler = Blockly.Python.statementToCode(block, 'HANDLER');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['thymio_event_prox_ground'] = function(block) {
  var dropdown_sensor = block.getFieldValue('SENSOR');
  var dropdown_mode = block.getFieldValue('MODE');
  var statements_handler = Blockly.Python.statementToCode(block, 'HANDLER');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['thymio_event_shock'] = function(block) {
  var statements_handler = Blockly.Python.statementToCode(block, 'HANDLER');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};