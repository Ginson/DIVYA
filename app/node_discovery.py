import os
import importlib
import inspect
from nodes.base_node import BaseNode

def get_node_classes():
    """
    Dynamically discovers and returns all BaseNode subclasses from the 
    nodes.built_in directory and the plugins directory.
    """
    node_classes = {}
    
    # --- Scan for built-in nodes ---
    scan_directory("nodes/built_in", node_classes)
    
    # --- Scan for plugin nodes ---
    scan_directory("plugins", node_classes, is_plugin=True)

    return node_classes

def scan_directory(directory, node_classes, is_plugin=False):
    """Scans a directory for node classes."""
    for item_name in os.listdir(directory):
        item_path = os.path.join(directory, item_name)
        
        if is_plugin:
            # For plugins, we look for .py files directly in the plugins folder
            if item_name.endswith(".py") and not item_name.startswith("__"):
                module_full_name = f"plugins.{item_name[:-3]}"
                load_nodes_from_module(module_full_name, node_classes)
        else:
            # For built-in nodes, we expect subdirectories for categories
            if os.path.isdir(item_path) and not item_name.startswith("__"):
                for module_name in os.listdir(item_path):
                    if module_name.endswith(".py") and not module_name.startswith("__"):
                        module_full_name = f"nodes.built_in.{item_name}.{module_name[:-3]}"
                        load_nodes_from_module(module_full_name, node_classes)

def load_nodes_from_module(module_full_name, node_classes):
    """Loads node classes from a given module."""
    try:
        module = importlib.import_module(module_full_name)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseNode) and obj is not BaseNode:
                node_name = obj().name
                if node_name in node_classes:
                    print(f"Warning: Duplicate node name '{node_name}' found. Overwriting.")
                node_classes[node_name] = obj
    except Exception as e:
        print(f"Error importing node from {module_full_name}: {e}")