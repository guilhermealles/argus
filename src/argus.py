import sys
import argparse
from core import main
from __init__ import __version__

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argus Backup Manager')
    parser.add_argument('--version', action='store_true', help='Display version information')
    parser.add_argument('--config', help='Path to the configuration file')
    
    args = parser.parse_args()
    
    if args.version:
        print(f"Argus Backup Manager v{__version__}")
        sys.exit(0)
    
    if not args.config:
        parser.error("the --config argument is required unless using --version")
    
    config_file = args.config
    
    sys.exit(main(config_file))