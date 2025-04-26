import subprocess
import logging
from config import read_config
from tasks import execute_task

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("argus")

def check_rclone():
    try:
        subprocess.run(["rclone", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def main(config_file):
    logger.info(f"Argus backup starting. Using config file: {config_file}")
    
    if not check_rclone():
        logger.error("rclone is not installed or not found in PATH. Please install rclone first.")
        return 1
    
    try:
        config = read_config(config_file)
    except Exception as e:
        logger.error(f"Failed to read config file: {e}")
        return 1
    
    global_exclude = config.get("global", {}).get("exclude", [])
    
    tasks = config.get("tasks", [])
    if not tasks:
        logger.warning("No tasks found in configuration file")
        return 0
    
    success_count = 0
    failed_count = 0
    
    for task in tasks:
        task_name = task.get("name", "unnamed-task")
        logger.info(f"Executing task: {task_name}")
        
        success = execute_task(task, global_exclude)
        if success:
            success_count += 1
            logger.info(f"Task completed successfully: {task_name}")
        else:
            failed_count += 1
            logger.error(f"Task failed: {task_name}")
    
    logger.info(f"Backup complete. {success_count} tasks succeeded, {failed_count} tasks failed.")
    
    return 0 if failed_count == 0 else 1 