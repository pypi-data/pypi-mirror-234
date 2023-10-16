"use strict";
/*
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ForceResizableOptions = exports.ForceDraggableOptions = exports.ForceNetwork = exports.Graph = exports.EdgeDataSet = exports.NodeDataSet = exports.Link = exports.IdentifiableDynamicObject = exports.Message = exports.VisEdge = exports.VisNode = exports.VisSelection = exports.DynamicObject = void 0;
const standalone_1 = require("vis-network/standalone");
const lodash_1 = require("lodash");
/**
 * Operates as a dictionary which we can add any key-value pair
 * such that the key is a string
 */
class DynamicObject {
}
exports.DynamicObject = DynamicObject;
class VisSelection {
    constructor(nodes, edges) {
        this.nodes = nodes;
        this.edges = edges;
    }
}
exports.VisSelection = VisSelection;
/**
 * Meant to be added to our Node datasets which requires an id.
 */
class VisNode {
    constructor(id) {
        this.id = id;
        this.id = id;
    }
    /**
     * Attempt to translate an IdentifiableDynamicObject into a VisNode.
     * Because an id is guaranteed, we will create a node only with that ID,
     * and then merge the remaining data in the object into the node afterwards.
     *
     * @remarks
     * lodash's merge functionality is used for this. You can find more information about
     * that here: https://lodash.com/docs/4.17.15#merge
     *
     * @param obj - An IdentifiableDynamicObject to turn into a node, with the obj.id being used for the node's id
     * @returns a VisNode whose id is obj.id
     */
    static fromObject(obj) {
        let node = new VisNode(obj.id);
        node = lodash_1.merge({}, obj, node);
        return node;
    }
    /**
     *
     * Takes an existing node and a DynamicObject, and merges the two,
     * taking the values of the DynamicObject as sources of truth.
     * @remarks
     * Note that this method will do a deep merge, meaning that if you have two
     * top-level properties whose key is "foo" and values are objects, those two
     * objects will be merged into the new value of "foo".
     */
    static mergeObject(node, obj) {
        if (obj === null || obj === undefined) {
            obj = {};
        }
        const copy = lodash_1.clone(node);
        return lodash_1.merge({}, copy, obj);
    }
}
exports.VisNode = VisNode;
/**
 * A VisEdge is meant to be added to a network's dataset containing edges.
 * We want to guarantee that each edge has a label for the purposes of displaying it.
 */
class VisEdge {
    constructor(from, to, id, label) {
        this.from = from;
        this.to = to;
        this.id = id;
        this.from = from;
        this.to = to;
        // make the edge id as unique as possible, while still being able to look it up.
        // visjs does not give us a mechanism to lookup an edge by its (from, to, id) tuple
        // so we combine them
        this.id = from + ":" + to + ":" + id;
        this.label = label;
    }
    /**
     * Attempt to translate a Dynamic object into a VisEdge.
     * For each required param a VisEdge must have, we will
     * look for that value and use it in the Edge, and then
     * merge the obj into the edge to grab and extra data it contains
     *
     * @remarks
     * lodash's merge functionality is used for this. You can find more information about
     * that here: https://lodash.com/docs/4.17.15#merge
     *
     * @param obj - an IdentifiableDynamicObject which is guaranteed to have an id
     * @returns a VisEdge whose 'from' 'to' and 'label' fields are picked up from the source object
     */
    static fromObject(obj) {
        const from = obj.hasOwnProperty("from") ? obj["from"] : "";
        const to = obj.hasOwnProperty("to") ? obj["to"] : "";
        const label = obj.hasOwnProperty("label") ? obj["label"] : obj.id;
        let edge = new VisEdge(from, to, obj.id, label);
        edge = lodash_1.merge({}, obj, edge);
        return edge;
    }
    /**
     * Takes an existing edge and a DynamicObject, and merges the two,
     * taking the values of the DynamicObject as sources of truth.
     * @remarks
     * Note that this method will do a deep merge, meaning that if you have two
     * top-level properties whose key is "foo" and values are objects, those two
     * objects will be merged into the new value of "foo".
     *
     * @param edge - The existing edge whose values will be overridden if there are conflicts.
     * @param obj - The DynamicObject to merge into the existing edge.
     *
     * @returns a new VisEdge whose values are combination of the original edge and obj, treating values in obj
     * as the new values of the edge.
     */
    static mergeObject(edge, obj) {
        if (obj === null || obj === undefined) {
            obj = {};
        }
        const copy = lodash_1.clone(edge);
        return lodash_1.merge({}, copy, obj);
    }
}
exports.VisEdge = VisEdge;
/**
 * Transmitted by the EventfulNetwork in the kernel.
 * A Message will always contain a method (such as 'add_node' and that methods'
 * corresponding inputs wrapped into the data object. The fields inside of data
 * will map to the input keys of the method the message represents. For example,
 * when add_node is called, we could receive a message like the following:
 {
    method: "add_node",
    data: {
        node_id: '1234',
        data: {
            label: 'SJC',
            type: 'airport'
        }
    }
}
 */
class Message {
    constructor(method, data) {
        this.method = method;
        this.data = data;
    }
}
exports.Message = Message;
/**
 * Extends a DynamicObject but is guaranteed to have an id field
 */
class IdentifiableDynamicObject extends DynamicObject {
    constructor(id) {
        super();
        this.id = id;
        this.id = id;
    }
}
exports.IdentifiableDynamicObject = IdentifiableDynamicObject;
/**
 * A Link is the networkx version of an edge, and must be translated to the representation which
 * visjs recognizes. They are the same except that networkx denotes an edge as source --> target
 * while visjs uses from --> to
 *
 * @remarks
 * More information can be found here: https://github.com/visjs/vis-network
 */
class Link {
    constructor(key, label, source, target) {
        this.key = key;
        this.label = label;
        this.source = source;
        this.target = target;
    }
}
exports.Link = Link;
/**
 * A vis-network Dataset based on a VisNode, whose identifying field is the "id"
 */
class NodeDataSet extends standalone_1.DataSet {
}
exports.NodeDataSet = NodeDataSet;
/**
 * A vis-network Dataset based on a VisEdge, whose identifying field is the "id"
 */
class EdgeDataSet extends standalone_1.DataSet {
}
exports.EdgeDataSet = EdgeDataSet;
/**
 * Inner structure of the ForceWidget's network traitlet, carried by the EventfulNetwork on the kernel which
 * serializes its MultiDiGraph into json. A graph is guaranteed to have an array of nodes
 * and an array of edges, either of which can be of 0 length.
 */
class Graph {
    constructor(nodes, links) {
        this.nodes = nodes;
        this.links = links;
    }
}
exports.Graph = Graph;
/**
 * The containing object for our graph which is used to convert between the ForceWidget's network traitlet
 * and json for use on the client-side.
 */
class ForceNetwork {
    constructor(graph) {
        this.graph = graph;
    }
}
exports.ForceNetwork = ForceNetwork;
class ForceDraggableOptions {
}
exports.ForceDraggableOptions = ForceDraggableOptions;
class ForceResizableOptions {
}
exports.ForceResizableOptions = ForceResizableOptions;
