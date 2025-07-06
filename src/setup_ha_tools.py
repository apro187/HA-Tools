#!/usr/bin/env python3
"""
setup_ha_tools.py

Copies the config.example.json to the user's config directory.
"""
import os
import json
import shutil
from ha_helpers.common import get_default_folders

def main():
    print("\n=== ha-tools Environment Setup ===\n")

    # Define paths
    base = os.path.expanduser('~/Documents/HA-Tools')
    config_dir = os.path.join(base, 'config')
    automations_dir = os.path.join(base, 'automations')
    scripts_dir = os.path.join(base, 'scripts')
    logs_dir = os.path.join(base, 'logs')
    prints_dir = config_dir

    # Create all folders if they don't exist
    for d in [base, config_dir, automations_dir, scripts_dir, logs_dir, prints_dir]:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
            print(f"Created directory: {d}")

    # Define the source and destination paths
    source_config_path = os.path.join(os.path.dirname(__file__), '..', 'config.example.json')
    dest_config_path = os.path.join(config_dir, 'config.json')

    # Check if a config file already exists
    if os.path.exists(dest_config_path):
        print(f"A configuration file already exists at {dest_config_path}")
        overwrite = input("Do you want to overwrite it? (y/n): ").lower()
        if overwrite not in ['y', 'yes']:
            print("Setup cancelled.")
            return

    # Copy the example config file
    try:
        shutil.copy(source_config_path, dest_config_path)
        print(f"Successfully copied config template to {dest_config_path}")
        print("\n--- Next Steps ---")
        print("1. Create a new PRIVATE Git repository to store your automations and scripts.")
        print("2. Clone the private repository to your local machine.")
        print(f"3. Open {dest_config_path} and update the following fields:")
        print("   - ha_url: Your Home Assistant URL (e.g., http://homeassistant.local:8123)")
        print("   - ha_token: Your Long-Lived Access Token.")
        print("   - automations_dir: The local path to your private automations repository.")
        print("   - scripts_dir: The local path to your private scripts repository.")
        print("\nSetup complete! You can now use ha-tools with your configuration.")

    except FileNotFoundError:
        print(f"Error: config.example.json not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
