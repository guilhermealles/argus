import subprocess
import logging

logger = logging.getLogger("argus.tasks")

def execute_task(task, global_exclude):
    """Execute a single backup task using rclone"""
    task_name = task.get("name", "unnamed-task")
    source_path = task["source"]["path"]
    destination_path = task["destination"]["path"]
    
    exclude_patterns = global_exclude.copy()
    task_exclude = task.get("exclude", [])
    if task_exclude:
        exclude_patterns.extend(task_exclude)

    command = ["rclone", "sync", source_path, destination_path]
    
    if exclude_patterns:
        for pattern in exclude_patterns:
            command.extend(["--exclude", pattern])
    
    command.extend([
        "--progress",
        "--stats", "1s",
        "--stats-one-line"
    ])
    
    logger.info(f"Running command: {' '.join(command)}")
    
    try:
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        
        if process.stdout:
            logger.debug(process.stdout)
        
        return True
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}: {e.stderr}")
        
        return False
    
    except Exception as e:
        logger.error(f"Error executing task '{task_name}': {str(e)}")
        
        return False 