/// <reference types="jqueryui" />
import { DataSet, Edge, Node } from "vis-network/standalone";
import DraggableOptions = JQueryUI.DraggableOptions;
import ResizableOptions = JQueryUI.ResizableOptions;
/**
 * Operates as a dictionary which we can add any key-value pair
 * such that the key is a string
 */
export declare class DynamicObject {
    [key: string]: any;
}
export declare class VisSelection {
    nodes: Array<string | number>;
    edges: Array<string | number>;
    constructor(nodes: Array<string | number>, edges: Array<string | number>);
}
/**
 * Meant to be added to our Node datasets which requires an id.
 */
export declare class VisNode implements Node, DynamicObject {
    readonly id: string;
    readonly id: string;
    [key: string]: any;
    constructor(id: string);
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
    static fromObject(obj: IdentifiableDynamicObject): VisNode;
    /**
     *
     * Takes an existing node and a DynamicObject, and merges the two,
     * taking the values of the DynamicObject as sources of truth.
     * @remarks
     * Note that this method will do a deep merge, meaning that if you have two
     * top-level properties whose key is "foo" and values are objects, those two
     * objects will be merged into the new value of "foo".
     */
    static mergeObject(node: VisNode, obj: DynamicObject): VisNode;
}
/**
 * A VisEdge is meant to be added to a network's dataset containing edges.
 * We want to guarantee that each edge has a label for the purposes of displaying it.
 */
export declare class VisEdge implements Edge {
    readonly from: string;
    readonly to: string;
    readonly id: string;
    readonly from: string;
    readonly to: string;
    readonly id: string;
    label: string;
    [key: string]: any;
    constructor(from: string, to: string, id: string, label: string);
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
    static fromObject(obj: IdentifiableDynamicObject): VisEdge;
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
    static mergeObject(edge: VisEdge, obj: DynamicObject): VisEdge;
}
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
export declare class Message {
    method: string;
    data: DynamicObject;
    constructor(method: string, data: object);
}
/**
 * Extends a DynamicObject but is guaranteed to have an id field
 */
export declare class IdentifiableDynamicObject extends DynamicObject {
    readonly id: string;
    readonly id: string;
    [key: string]: any;
    constructor(id: string);
}
/**
 * A Link is the networkx version of an edge, and must be translated to the representation which
 * visjs recognizes. They are the same except that networkx denotes an edge as source --> target
 * while visjs uses from --> to
 *
 * @remarks
 * More information can be found here: https://github.com/visjs/vis-network
 */
export declare class Link {
    key: string;
    label: string;
    source: string;
    target: string;
    [key: string]: any;
    constructor(key: string, label: string, source: string, target: string);
}
/**
 * A vis-network Dataset based on a VisNode, whose identifying field is the "id"
 */
export declare class NodeDataSet extends DataSet<VisNode, "id"> {
    [key: string]: any;
}
/**
 * A vis-network Dataset based on a VisEdge, whose identifying field is the "id"
 */
export declare class EdgeDataSet extends DataSet<VisEdge, "id"> {
    [key: string]: any;
}
/**
 * Inner structure of the ForceWidget's network traitlet, carried by the EventfulNetwork on the kernel which
 * serializes its MultiDiGraph into json. A graph is guaranteed to have an array of nodes
 * and an array of edges, either of which can be of 0 length.
 */
export declare class Graph {
    nodes: VisNode[];
    links: Link[];
    constructor(nodes: VisNode[], links: Link[]);
}
/**
 * The containing object for our graph which is used to convert between the ForceWidget's network traitlet
 * and json for use on the client-side.
 */
export declare class ForceNetwork {
    graph: Graph;
    constructor(graph: Graph);
}
export declare class ForceDraggableOptions implements DraggableOptions {
}
export declare class ForceResizableOptions implements ResizableOptions {
}
