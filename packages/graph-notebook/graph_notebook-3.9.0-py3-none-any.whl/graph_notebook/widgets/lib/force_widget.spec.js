"use strict";
/*
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
 */
Object.defineProperty(exports, "__esModule", { value: true });
const types_1 = require("./types");
const chai_1 = require("chai");
const sinon_1 = require("sinon");
describe("force_widget", function () {
    describe("Message", function () {
        it("should initalize a message", function () {
            const method = "test";
            const data = { a: 1 };
            const message = new types_1.Message(method, data);
            chai_1.assert.equal(method, message.method);
            chai_1.assert.deepEqual(data, message.data);
        });
    });
    describe("console", function () {
        it("should log an info", function () {
            const consoleSpy = sinon_1.spy(console, "info");
            const message = "test";
            const data = { a: 1 };
            console.info(message, data);
            chai_1.expect(consoleSpy.calledWith(message, data)).to.be.ok;
        });
    });
});
