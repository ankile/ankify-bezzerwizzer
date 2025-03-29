#!/usr/bin/env python3
import os
import sys
import glob

def create_numbered_folder():
    """Create a new folder under 'cards' with incremental number as name (001, 002, etc.)."""
    # Ensure the base 'cards' directory exists
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards")
    os.makedirs(base_dir, exist_ok=True)
    
    # Find existing numbered folders
    existing_folders = glob.glob(os.path.join(base_dir, "[0-9][0-9][0-9]"))
    
    # Determine the next folder number
    if existing_folders:
        # Extract the numeric parts and find the max
        folder_numbers = [int(os.path.basename(folder)) for folder in existing_folders]
        next_number = max(folder_numbers) + 1
    else:
        # Start with 001 if no folders exist
        next_number = 1
    
    # Format as 3-digit string (001, 002, etc.)
    folder_name = f"{next_number:03d}"
    
    # Create the new folder
    new_folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    
    print(f"Created folder: {new_folder_path}")
    return new_folder_path

if __name__ == "__main__":
    folder_path = create_numbered_folder()
    # If run with --open flag, open the folder in the file explorer
    if len(sys.argv) > 1 and sys.argv[1] == "--open":
        if sys.platform == "darwin":  # macOS
            os.system(f"open '{folder_path}'")
        elif sys.platform == "win32":  # Windows
            os.system(f'explorer "{folder_path}"')
        elif sys.platform.startswith("linux"):  # Linux
            os.system(f"xdg-open '{folder_path}'")