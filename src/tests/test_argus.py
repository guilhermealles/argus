#!/usr/bin/env python3

"""
A simple test script to verify Argus functionality without actually running rclone.
This is done by mocking the subprocess.run function.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import main
from config import read_config
from tasks import execute_task

class TestArgus(unittest.TestCase):
    
    def test_config_reading(self):
        """Test that config file is read correctly"""
        config_file = os.path.join(os.path.dirname(__file__), "resources/test.config.json")
        config = read_config(config_file)
        
        self.assertIn("global", config)
        self.assertIn("tasks", config)
        self.assertIsInstance(config["tasks"], list)
        
        task = config["tasks"][0]
        self.assertEqual(task["name"], "test-task")
        self.assertEqual(task["source"]["path"], "/test/source")
        self.assertEqual(task["destination"]["path"], "remote:/test/dest")
    
    @patch('subprocess.run')
    def test_task_execution(self, mock_run):
        """Test that tasks are executed with the correct commands"""
        # Mock subprocess.run to return a successful result
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Sync completed successfully"
        mock_run.return_value = mock_process
        
        # Create a test task
        task = {
            "name": "test-task",
            "source": {"path": "/test/source"},
            "destination": {"path": "remote:/test/dest"}
        }
        
        result = execute_task(task, ["**/DS_Store/**"])
        
        mock_run.assert_called_once()
        
        args = mock_run.call_args[0][0]
        self.assertEqual(args[0], "rclone")
        self.assertEqual(args[1], "sync")
        self.assertEqual(args[2], "/test/source")
        self.assertEqual(args[3], "remote:/test/dest")
        
        self.assertIn("--exclude", args)
        self.assertIn("**/DS_Store/**", args)

        self.assertTrue(result)
    
    @patch('subprocess.run')
    @patch('core.check_rclone')
    def test_main_function(self, mock_check_rclone, mock_run):
        """Test the main function"""
        mock_check_rclone.return_value = True
        
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Sync completed successfully"
        mock_run.return_value = mock_process
        
        config_file = os.path.join(os.path.dirname(__file__), "resources/test.config.json")
        
        result = main(config_file)
        
        self.assertEqual(result, 0)
        
        mock_run.assert_called()

if __name__ == "__main__":
    unittest.main() 