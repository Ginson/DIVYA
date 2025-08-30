from app.core.graph import Graph
from nodes.base_node import BaseNode
from typing import Dict, List
from collections import deque

class Engine:
    """Executes the graph by processing nodes in the correct order."""
    def process(self, graph: Graph):
        # Perform topological sort to find execution order
        sorted_nodes = self._topological_sort(graph)
        if not sorted_nodes:
            print("Error: Graph has a cycle or is empty.")
            return

        print("--- Executing Graph ---")
        # Store outputs of executed nodes
        node_outputs_cache = {}

        for node_id in sorted_nodes:
            node = graph.nodes[node_id]
            print(f"Executing Node: {node.name}")

            # Gather inputs for the current node from the cache
            inputs_for_node = self._get_inputs_for_node(node, graph, node_outputs_cache)
            
            # Execute the node's logic
            result = node.execute(**inputs_for_node)
            
            # Cache the results for downstream nodes
            node_outputs_cache[node.id] = result
        
        print("--- Graph Execution Finished ---")

    def _get_inputs_for_node(self, node: BaseNode, graph: Graph, cache: Dict) -> Dict:
        """Finds and retrieves the inputs for a given node from the cache."""
        inputs = {}
        for edge in graph.edges.values():
            if edge.target_node_id == node.id:  # If this edge connects to the current node
                if edge.source_node_id in cache:
                    inputs[edge.target_input_name] = cache[edge.source_node_id].get(edge.source_output_name)
        return inputs

    def _topological_sort(self, graph: Graph) -> List[str]:
        """Determinines the correct order to execute nodes."""
        in_degree = {node_id: 0 for node_id in graph.nodes}
        adj = {node_id: [] for node_id in graph.nodes}

        for edge in graph.edges.values():
            in_degree[edge.target_node_id] += 1
            adj[edge.source_node_id].append(edge.target_node_id)
        
        queue = deque([node_id for node_id, degree in in_degree.items() if degree == 0])
        sorted_order = []

        while queue:
            node_id = queue.popleft()
            sorted_order.append(node_id)
            for neighbor in adj[node_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(sorted_order) == len(graph.nodes):
            return sorted_order
        return [] # Cycle detected