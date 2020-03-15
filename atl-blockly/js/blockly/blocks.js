/**
 * @license
 * Visual Blocks Editor
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

goog.provide('Blockly.Blocks.atl');

goog.require('Blockly.Blocks');

Blockly.Blocks['cozmo_on_start'] = {
  init: function() {
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_CENTRE)
        .appendField(new Blockly.FieldImage("http://localhost:9090/static/ATL-Logo.png", 15, 15, { alt: "*", flipRtl: "FALSE" }))
        .appendField(Blockly.Msg.COZMO_ON_START_01);
    this.appendDummyInput()
        .appendField(Blockly.Msg.COZMO_ON_START_03)
        .appendField(new Blockly.FieldDropdown([["0",'0'], ["1",'1'], ["2",'2'], ["3",'3']]), "DEBUG_LEVEL");
    this.appendStatementInput("BODY");
    this.setColour(Blockly.Blocks.cozmo.HUE2);
    this.setTooltip(Blockly.Msg.COZMO_ON_START_02);
  }
};

Blockly.Blocks['atl_shuffle_the_list'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("http://localhost:9090/static/ATL-Logo.png", 15, 15, { alt: "*", flipRtl: "FALSE" }));
    this.appendDummyInput()
        .appendField(Blockly.Msg.ATL_SHUFFLE_THE_LIST_01);
    this.appendValueInput("ATL_LIST")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(330);
 this.setTooltip(Blockly.Msg.ATL_SHUFFLE_THE_LIST_02);
 this.setHelpUrl("");
  }
};


Blockly.Blocks['atl_comment'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("http://localhost:9090/static/ATL-Logo.png", 15, 15, { alt: "*", flipRtl: "FALSE" }));
    this.appendDummyInput()
        .appendField(Blockly.Msg.ATL_COMMENT_01);
    this.appendValueInput("ATL_COMMENT_IN_CODE_TEXT")
        .setCheck("String");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
 this.setTooltip(Blockly.Msg.ATL_COMMENT_02);
 this.setHelpUrl("");
  }
};

Blockly.Blocks['atl_print'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldImage("http://localhost:9090/static/ATL-Logo.png", 15, 15, { alt: "*", flipRtl: "FALSE" }));
    this.appendDummyInput()
        .appendField(Blockly.Msg.ATL_PRINT_01);
    this.appendValueInput("ATL_PRINT")
        .setCheck(null);
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(330);
 this.setTooltip(Blockly.Msg.ATL_PRINT_02);
 this.setHelpUrl("");
  }
};