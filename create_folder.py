#!/usr/bin/env python3
import os
import datetime
import sys

def create_timestamped_folder():
    """Create a new folder under 'cards' with current timestamp as name."""
    # Get current timestamp in format YYYY-MM-DD-HH-MM-SS
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    # Ensure the base 'cards' directory exists
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards")
    os.makedirs(base_dir, exist_ok=True)
    
    # Create the new timestamped folder
    new_folder_path = os.path.join(base_dir, timestamp)
    os.makedirs(new_folder_path, exist_ok=True)
    
    print(f"Created folder: {new_folder_path}")
    return new_folder_path

if __name__ == "__main__":
    folder_path = create_timestamped_folder()
    # If run with --open flag, open the folder in the file explorer
    if len(sys.argv) > 1 and sys.argv[1] == "--open":
        if sys.platform == "darwin":  # macOS
            os.system(f"open '{folder_path}'")
        elif sys.platform == "win32":  # Windows
            os.system(f'explorer "{folder_path}"')
        elif sys.platform.startswith("linux"):  # Linux
            os.system(f"xdg-open '{folder_path}'")