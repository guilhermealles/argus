# Argus Backup Manager

A simple backup manager built on top of `rclone`.

## Requirements

- Python 3.6+
- rclone (must be configured and available in PATH)

## Usage

Argus works by defining tasks. Each task represents a directory to be synced between source and destination. Since Argus works on top of rclone, both source and destination can be remote locations.

1. Create a configuration file (see example below)
2. Run Argus with the configuration file:

   Using the wrapper script:
   ```
   ./argus.sh --config path/to/config.json
   ```

   You can also use relative or absolute paths:
   ```
   ./argus.sh --config ../config/argus.config.json
   ./argus.sh --config ./config/argus.config.json
   ```

   To display version information:
   ```
   ./argus.sh --version
   ```

3. (Optional) Schedule periodic execution with cron, launchd or others

## Configuration

Argus uses a JSON configuration file with the following structure:

```json
{
  "global": {
    "exclude": ["**/DS_Store/**", "**/*.tmp", "**/node_modules/**"]
  },
  "tasks": [
    {
      "name": "documents-backup",
      "source": {
        "path": "/path/to/local/documents"
      },
      "destination": {
        "path": "remote-name:/path/on/remote"
      },
      "exclude": ["**/private/**"]
    },
    {
      "name": "photos-backup",
      "source": {
        "path": "photos-remote:/photos"
      },
      "destination": {
        "path": "another-remote:/photos"
      }
    }
  ]
}
```

### Configuration Options

- `global`: Global settings that apply to all tasks
  - `exclude`: Array of glob patterns for files/folders to exclude
- `tasks`: Array of backup tasks to execute
  - `name`: A name for the task (used in logs)
  - `source`: The source location
    - `path`: Path to the source directory
  - `destination`: The destination location
    - `path`: Path to the destination
  - `exclude`: Task-specific exclude patterns (optional)

## Important Notes

1. You must have already configured rclone remotes before using them in Argus.
2. For now, Argus uses rclone's `sync` command. This means files deleted from the source will also be deleted from the destination.

## Next steps

- Improve logging
- Incremental backup tasks