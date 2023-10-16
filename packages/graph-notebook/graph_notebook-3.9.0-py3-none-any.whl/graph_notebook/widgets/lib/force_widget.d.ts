import { DOMWidgetModel, DOMWidgetView, ISerializers } from "@jupyter-widgets/base";
import { DynamicObject, ForceNetwork, Link, Message, VisEdge, VisNode } from "./types";
import "jquery-ui/ui/widgets/draggable";
import "jquery-ui/ui/widgets/resizable";
import "../css/widget.css";
export declare class ForceModel extends DOMWidgetModel {
    defaults(): any;
    static serializers: ISerializers;
    static model_name: string;
    static model_module: any;
    static model_module_version: any;
    static view_name: string;
    static view_module: any;
    static view_module_version: any;
}
export declare class ForceView extends DOMWidgetView {
    private networkDiv;
    private canvasDiv;
    private menu;
    private expandDiv;
    private searchDiv;
    private searchOptionsDiv;
    private resetDiv;
    private detailsDiv;
    private physicsDiv;
    private nodeDataset;
    private edgeDataset;
    private visOptions;
    private vis;
    private detailsPanel;
    private detailsHeader;
    private graphPropertiesTable;
    private emptyDetailsMessage;
    private graphTableDiv;
    private resizeHandle;
    private detailsContainer;
    private noDataMessage;
    private noElementSelectedMessage;
    private expandBtn;
    private nodeIDSearchMatches;
    private edgeIDSearchMatches;
    private excludeIDsFromSearch;
    private closeButton;
    private detailsText;
    private searchOptionsBtn;
    private searchMatchColorEdge;
    private searchMatchColorNode;
    private resetBtn;
    private doingReset;
    private detailsBtn;
    private selectedNodeID;
    private physicsBtn;
    render(): void;
    /**
     * Take the json from a given network, and update our datasets
     * used to render the vis Network.
     *
     * @remarks
     * Used at the initial rendering of the force widget, or any time
     * we override the network entirely
     *
     * @param network - The network to update this ForceView's datasets
     */
    populateDatasets(network: ForceNetwork): void;
    /**
     * Triggered when the network traitlet on the Kernel-side is overridden. In this case,
     * the currently rendered network will cleared with the nodes and links present in the new network
     */
    changeNetwork(): void;
    /**
     * Triggered when the options traitlet is overridden on the Kernel-side. This will trigger updating the
     * options of the vis rendering.
     */
    changeOptions(): void;
    /**
     * Returns a modified visOptions, with the custom simulationDuration and disablePhysicsAfterInitialSimulation physics
     * options removed. This prevents an error from being thrown when VisJS parses visOptions.
     */
    stripCustomPhysicsOptions(): any;
    /**
     * Take custom messages from the kernel and route them to the appropriate handler.
     * Each custom message will have a method field, and a corresponding data field which contains the payload
     * from the message.
     *
     * @remarks
     * NOTE: The method field is only present because all our custom messages build their payloads in this
     * fashion.
     */
    interceptCustom(msg: Message): void;
    /**
       * Add a node to the nodes dataset, merging the new node with the existing one
       * if this id is already present.
       *
       * The payload coming to this handler from the Kernel will look like:
       {
            "node_id": "1234",
            "data": {
              "label": "SJC",
              "properties": {
                "type": "airport",
                "runways": "4"
              }
            }
          }
       */
    addNode(msgData: DynamicObject): void;
    /**
       * Handler to add new data to a node. The input to this is the same as the input to
       * adding a node, because adding a node checks for whether a given id existed,
       * and merges them if the node does.
       *
       * Example input:
       {
            "node_id": "1234",
            "data": {
              "properties": {
                "new_prop": "value"
              }
            }
          }
       */
    addNodeData(msgData: DynamicObject): void;
    /**
       * Add a key-value pair to a node under its "properties" field
       * If the node does not exist, we will create it with this property.
       * Example input:
  
       {
            "node_id": "1234",
            "key": "foo",
            "value": "bar"
          }
  
       * Example result:
       {
            "node_id": "1234",
            "data": {
              "label": "SJC",
              "properties": {
                "type": "airport",
                "runways": "4",
                "foo": "bar"
              }
            }
          }
       */
    addNodeProperty(msgData: DynamicObject): void;
    /**
       * Add an edge to the edgeDataset. Before attempting to add an edge, we will
       * ensure that it has the fields we need to create a VisEdge as they are represented
       * by the add_edge EventfulNetwork method. That payload looks like:
       *
       * @remarks
       * NOTE: we have two different labels here because the top-level "label" is used for displaying,
       * while the inner "properties" label field is the actual value that the underlying structure had.
       * For example, for GremlinNetworks, each edge will have a label, but a user might want to choose the property
       * "code" for us in displaying. In that case, the value of the property "code" would be set to the top-level
       * "label" field.
       {
            "edge_id": "to",
            "from_id": "MKE2DFW",
            "label": "to",
            "to_id": "DFW",
            "data": {
              "label": "to"
            }
       }
       */
    addEdge(msgData: DynamicObject): void;
    /**
     * Handler to add more data to an edge. The received payload is identical to
     * that of adding an edge, so we defer to that handler instead.
     */
    addEdgeData(data: DynamicObject): void;
    /**
     * Convert networkx links to Edges. To do this, we want to convert
     * "source" into "from"
     * "target" into "to"
     * and "key" into "id"
     *
     * @remarks
     * This is performed anytime we override the network which is backing this visualization.
     */
    linksToEdges(links: Array<Link>): Array<VisEdge>;
    /**
     * Handler to route events observed on the vis network.
     */
    registerVisEvents(): void;
    /**
     * handle deselecting any number of nodes, ensuring the a node which was selected and is a current valid
     * search match does not recieve the wrong border color indicating a search match.
     * @param nodeID
     */
    handleDeselectNode(nodeID: string | number): void;
    /**
     * When an empty click is detected, the details panel needs to be cleared to show the appropriate message
     */
    handleEmptyClick(): void;
    /**
     * Hide the generated table of graph properties and show an empty message
     */
    hideGraphProperties(): void;
    /**
     * Build the Properties section of the details panel from a given node or edge.
     *
     * @param data - a node or edge
     */
    buildGraphPropertiesTable(data: VisNode | VisEdge): void;
    /**
     * ensure that the table containing graph properties is visible, and that the empty
     * message advising the user to select a node or edge is hidden
     */
    showGraphProperties(): void;
    setDetailsMessage(message: string): void;
    /**
     * Take an arbitrary object and convert its kvps into tr elements
     * with two columns. The first column is the key, the second is the value.
     *
     * @param data - a dictionary to turn into rows of a table
     */
    buildTableRows(data: DynamicObject): Array<HTMLElement>;
    /**
     * Handle a single node being clicked. This will build details tables for all
     * key-value pairs which are on the edge. all key-value pairs which appear under the
     * "properties" top-level key will be treated as data which exists on the graph which
     * was queried to gather this data. All others are treated as data which is used by vis.
     *
     * @param nodeID - the id of the edge as represented by this.vis
     */
    handleNodeClick(nodeID: string | number): void;
    /**
     * Handle a single edge being clicked. This will build details tables for all
     * key-value pairs which are on the edge. all key-value pairs which appear under the
     * "properties" top-level key will be treated as data which exists on the graph which
     * was queried to gather this data. All others are treated as data which is used by vis.
     *
     * @param edgeID - the id of the edge as represented by this.vis
     */
    handleEdgeClick(edgeID: string | number): void;
    /**
     * Searches for the provided text under all nodes and edges in this.vis
     * If any property or key contains the text, that edge or node will be highlighted
     *
     * NOTE: Case sensitive.
     * @param text - The content to search for
     */
    handleSearchInput(text: string): void;
    /**
     * Builds the side panel of actions and any other elements that they rely on.
     * Currently, this includes action icons for Search, Details, and Maximize
     * as well as a panel which is revealed when the details action is toggled.
     * This extra panel will show the details of a given selected node.
     */
    buildActions(): void;
    handleDetailsToggle(): void;
    /**
     * Search the provided data for an instance of the given text
     * @param text - the search term
     * @param data - data to be searched
     * @param excludeIDs - boolean indicating whether we want to highlight ID matches
     */
    search(text: string, data: any, depth: number, excludeIDs: boolean): boolean;
    /**
     * Take this widget to full screen mode, ensuring that the positioning of the details
     * panel remains in the same relative position that it was in before full screen mode.
     */
    toggleExpand(): void;
    /**
     * Register any needed events to this.el, the containing element for this widget
     */
    registerWidgetEvents(): void;
}
