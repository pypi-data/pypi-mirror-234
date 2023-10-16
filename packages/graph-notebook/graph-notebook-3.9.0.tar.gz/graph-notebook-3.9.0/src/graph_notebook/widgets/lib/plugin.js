"use strict";
/*
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
 */
Object.defineProperty(exports, "__esModule", { value: true });
const base_1 = require("@jupyter-widgets/base");
const force_widget_1 = require("./force_widget");
const version_1 = require("./version");
const EXTENSION_ID = "graph_notebook_widgets:plugin";
/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app, registry) {
    registry.registerWidget({
        name: version_1.MODULE_NAME,
        version: version_1.MODULE_VERSION,
        exports: { ForceModel: force_widget_1.ForceModel, ForceView: force_widget_1.ForceView },
    });
}
/**
 * The example plugin.
 */
const plugin = {
    id: EXTENSION_ID,
    requires: [base_1.IJupyterWidgetRegistry],
    activate: activateWidgetExtension,
    autoStart: true,
};
exports.default = plugin;
