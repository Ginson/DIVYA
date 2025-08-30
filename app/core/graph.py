# file: app/core/graph.py

from dataclasses import dataclass
from typing import Dict, Optional

from nodes.base_node import BaseNode

@dataclass
class Edge:
    """Represents a connection from one node's output to another's input."""
    source_node_id: str
    source_output_name: str
    target_node_id: str
    target_input_name: str

class Graph:
    """
    Manages the data model of the node graph, including all nodes and edges.
    """
    def __init__(self):
        self.nodes: Dict[str, BaseNode] = {}
        self.edges: Dict[str, Edge] = {}

    def add_node(self, node: BaseNode):
        """Adds a node instance to the graph."""
        if node.id in self.nodes:
            raise ValueError(f"Node with ID {node.id} already exists.")
        self.nodes[node.id] = node

    def add_edge(self, source_node_id: str, source_output: str, target_node_id: str, target_input: str):
        """Adds an edge, creating a connection between two nodes."""
        if source_node_id not in self.nodes or target_node_id not in self.nodes:
            raise KeyError("Cannot create edge: source or target node not found in graph.")

        # Create a unique identifier for the edge to prevent duplicates
        edge_id = f"{source_node_id}:{source_output}->{target_node_id}:{target_input}"

        if edge_id in self.edges:
            print(f"Warning: Edge {edge_id} already exists.")
            return

        edge = Edge(source_node_id, source_output, target_node_id, target_input)
        self.edges[edge_id] = edge

    def get_node(self, node_id: str) -> Optional[BaseNode]:
        """Retrieves a node from the graph by its ID."""
        return self.nodes.get(node_id)

    def __repr__(self) -> str:
        """Provides a summary of the graph's state."""
        return f"Graph with {len(self.nodes)} nodes and {len(self.edges)} edges."

    def remove_node(self, node_id: str):
        """Removes a node and any connected edges."""
        if node_id not in self.nodes:
            return

        # Remove the node itself
        del self.nodes[node_id]

        # Remove all edges connected to this node
        edges_to_remove = [
            edge_id for edge_id, edge in self.edges.items()
            if edge.source_node_id == node_id or edge.target_node_id == node_id
        ]
        for edge_id in edges_to_remove:
            del self.edges[edge_id]

    def remove_edge(self, edge_id: str):
        """Removes an edge by its unique ID."""
        if edge_id in self.edges:
            del self.edges[edge_id]

    def serialize(self):
        """Serializes the graph to a dictionary."""
        nodes_data = []
        for node in self.nodes.values():
            nodes_data.append({
                'id': node.id,
                'name': node.name,
                'parameters': node.param_values,
                'pos': [node.ui_node.x(), node.ui_node.y()] if hasattr(node, 'ui_node') else [0, 0]
            })

        edges_data = []
        for edge in self.edges.values():
            edges_data.append({
                'source_node_id': edge.source_node_id,
                'source_output_name': edge.source_output_name,
                'target_node_id': edge.target_node_id,
                'target_input_name': edge.target_input_name
            })

        return {'nodes': nodes_data, 'edges': edges_data}

    def clear(self):
        """Clears the graph."""
        self.nodes.clear()
        self.edges.clear()

    def deserialize(self, data, node_classes):
        """Deserializes the graph from a dictionary."""
        self.clear()

        for node_data in data['nodes']:
            node_name = node_data['name']
            if node_name in node_classes:
                node_class = node_classes[node_name]
                node = node_class()
                node.id = node_data['id']
                node.param_values = node_data['parameters']
                if 'pos' in node_data:
                    # This is a bit of a hack, we'll store the position and use it later
                    node.temp_pos = node_data['pos']
                self.add_node(node)
            else:
                print(f"Warning: Node class '{node_name}' not found.")

        for edge_data in data['edges']:
            self.add_edge(
                edge_data['source_node_id'],
                edge_data['source_output_name'],
                edge_data['target_node_id'],
                edge_data['target_input_name']
            )
