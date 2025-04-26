import os
import json
import logging

logger = logging.getLogger("argus.config")

def read_config(config_file):
    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file: {config_file}")
    
    validate_config(config)
    
    return config

def validate_config(config):
    if "tasks" not in config:
        raise ValueError("No 'tasks' section found in configuration")
    
    if not isinstance(config["tasks"], list):
        raise ValueError("'tasks' must be a list")
    
    for i, task in enumerate(config["tasks"]):
        task_name = task.get("name", f"task-{i}")
        
        if "source" not in task:
            raise ValueError(f"Missing 'source' in task '{task_name}'")
        
        if "destination" not in task:
            raise ValueError(f"Missing 'destination' in task '{task_name}'")
        
        if "path" not in task["source"]:
            raise ValueError(f"Missing 'path' in 'source' for task '{task_name}'")
        
        if "path" not in task["destination"]:
            raise ValueError(f"Missing 'path' in 'destination' for task '{task_name}'")
    
    if "global" in config and not isinstance(config["global"], dict):
        raise ValueError("'global' must be an object/dictionary")
    
    return True 