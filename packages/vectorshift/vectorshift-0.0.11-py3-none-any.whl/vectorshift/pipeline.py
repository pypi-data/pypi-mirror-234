# functionality to stitch together nodes into pipelines
from collections import defaultdict
import json 
from typing import List
from networkx import MultiDiGraph, topological_generations

from node import *
from consts import *

# Helpers for converting to JSON
# Assign a width and height to a node.
def assign_node_size(node:NodeTemplate):
    if type(node) in [InputNode, OutputNode]:
        return 250, 155
    elif type(node) in [URLLoaderNode, FileLoaderNode]:
        return 200, 100
    elif type(node) in [OpenAILLMNode, VectorDBLoaderNode, VectorDBReaderNode]:
        return 275, 175
    return 275, 250

# Assign a position (x,y) to a node. TODO: Right now this function is 
# rudimentary, arranging all nodes in a straight line.
def assign_node_positions(nodes:list[NodeTemplate], edges:list[dict]):
    # Generate a graph with just the relevant data from the nodes and edges
    nodes = [node._id for node in nodes]
    edges = [(edge['source'], edge['target'], {
        'sourceHandle': edge['sourceHandle'].replace(f'{edge["source"]}-', '', 1),
        'targetHandle': edge['targetHandle'].replace(f'{edge["target"]}-', '', 1)
    }) for edge in edges]

    G = MultiDiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Sort the nodes into topological generations
    top_gen = topological_generations(G)

    # Assign positions to each node, aligning the nodes within each generation vertically
    # and centered about the x-axis
    positions = {}
    for i, generation in enumerate(top_gen):
        for j, node in enumerate(generation):
            positions[node] = {'x': i * 400, 'y': (j - len(generation) // 2) * 400}

    return positions

# Create a pipeline by passing in nodes and params in.
class Pipeline():
    def __init__(self, name:str, description:str, nodes:List[NodeTemplate]):
        self.name = name 
        self.description = description 
        self.nodes = nodes
        # Assign node IDs and gather ID (node type) counts; also record the 
        # inputs and outputs
        # NB: in a node's JSON representation, id, type, data.id, and 
        # data.nodeType are essentially the same
        node_type_counts = defaultdict(int)
        # The OVERALL pipeline input and output nodes, keyed by node IDs 
        # (analogous to Mongo)
        self.inputs, self.outputs = {}, {}
        for n in self.nodes:
            t = n.node_type
            type_counter = node_type_counts[t] + 1
            node_id = f"{t}-{type_counter}"
            n._id = node_id
            node_type_counts[t] = type_counter
            if type(n) == InputNode:
                self.inputs[node_id] = {"name": n.name, "type": n.input_type.capitalize()}
            elif type(n) == OutputNode:
                self.outputs[node_id] = {"name": n.name, "type": n.output_type.capitalize()}
        self.node_type_counts = dict(node_type_counts)
        
        # Create edges: An edge is a dict following the JSON structure. All 
        # edges in the computation graph defined by the nodes terminate at some
        # node, i.e. are in the node's _inputs. So it should suffice to parse
        # through every node's _inputs and create an edge for each one. 
        self.edges = []
        for n in self.nodes:
            # n.inputs() is a dictionary of input field names to NodeOutputs 
            # from ancestor nodes filling those fields
            target_node_id = n._id
            for input_field, output in n.inputs().items():
                # Edges are specifically defined by source/target handles, 
                # derived from the node ids
                source_node_id = output.source._id
                output_field = output.output_field
                source_handle = f"{source_node_id}-{output_field}"
                target_handle = f"{target_node_id}-{input_field}"
                # Create an edge id following ReactFlow's formatting
                id = f"reactflow__edge-{source_node_id}{source_handle}-{target_node_id}{target_handle}"
                self.edges.append({
                    "source": source_node_id,
                    "sourceHandle": source_handle,
                    "target": target_node_id,
                    "targetHandle": target_handle,
                    "id": id
                })
    
    # Convert a Pipeline into a JSON string.  
    def to_json_rep(self):
        node_sizes = [assign_node_size(n) for n in self.nodes]
        node_positions = assign_node_positions(self.nodes, self.edges)
        node_jsons = []
        for i, node in enumerate(self.nodes):
            # we currently fix the position and absolute position to be the same
            node_display_params = {
                "position": node_positions[node._id],
                "positionAbsolute": node_positions[node._id],
                "width": node_sizes[i][0],
                "height": node_sizes[i][1],
                "selected": False,
                "dragging": False
            }
            node_json = self.nodes[i].json_rep()
            node_jsons.append({**node_json, **node_display_params})
        # TODO: these edge display params are also fixed for now
        edge_display_params = {
            "type": "smoothstep",
            "animated": True,
            "markerEnd": {
                "type": "arrow",
                "height": "20px",
                "width": "20px"
            }
        }
        edge_jsons = [{**e, **edge_display_params} for e in self.edges]
        return {
            # The overall (top-level) _id field for the JSON is gen'd by Mongo.
            "name": self.name,
            "description": self.description,
            "nodes": node_jsons,
            "edges": edge_jsons,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "nodeIDs": self.node_type_counts,
            # TODO: should this always be false?
            "zipOutputs": False,
        }
    
    def to_json(self):
        return json.dumps(self.to_json_rep(), indent=4)