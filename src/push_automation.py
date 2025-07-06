#!/usr/bin/env python3
"""
push_automation.py

Pushes Home Assistant automations and scripts to your HA instance via the REST API.

- Supports pushing all YAML files in automations/scripts folders, a single file,
  or auto-detecting changes since the last git commit.
- Can auto-overwrite existing automations/scripts with confirmation or --auto-overwrite flag.
- Lints YAML before pushing and checks for existing entities.
"""
import os
import glob
import yaml
import json
import requests
import argparse
from pathlib import Path
import git
from ha_helpers.common import get_config, get_config_path

# Global flag for auto-overwrite
AUTO_OVERWRITE = False

def print_error(msg):
    print(f"\033[91m{msg}\033[0m")

def get_changed_yaml_files():
    """Returns a list of changed YAML files since the last commit."""
    try:
        repo = git.Repo(search_parent_directories=True)
        
        # Compare HEAD with HEAD~1 to get only files changed in the last commit
        # This assumes the user has already committed their changes.
        if len(repo.heads) == 0:
            print("No commits found in the repository.")
            return []
        
        if len(repo.heads[0].commit.parents) == 0:
            print("Only one commit found. Cannot compare with previous commit.")
            return []

        diff_index = repo.head.commit.diff(repo.head.commit.parents[0])
        
        changed_files = []
        for item in diff_index:
            if item.change_type in ('A', 'M', 'R'): # Added, Modified, Renamed
                if item.b_path and item.b_path.endswith(('.yaml', '.yml')):
                    changed_files.append(item.b_path)
            elif item.change_type == 'D': # Deleted
                # We don't push deleted files, but we might want to log them or handle them differently
                pass
        
        if not changed_files:
            print("No new YAML files detected in the last commit.")
            return []

        # Return full paths
        return [os.path.join(repo.working_dir, f) for f in changed_files]
    except git.InvalidGitRepositoryError:
        print_error(f"Error: The current directory is not a Git repository. Please run this script from within your automations/scripts repository.")
        return []
    except Exception as e:
        print_error(f"An error occurred while detecting git changes: {e}")
        return []

def push_file(filepath, ha_config, auto_overwrite=False):
    """Pushes a single automation or script file to Home Assistant."""
    try:
        with open(filepath, 'r') as f:
            content = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print_error(f"Error reading YAML file {filepath}: {e}")
        return
    except FileNotFoundError:
        print_error(f"File not found: {filepath}")
        return

    if not isinstance(content, dict) or ('id' not in content and 'alias' not in content):
        print_error(f"Invalid format in {filepath}. Each automation/script must be a dictionary with an 'id' or 'alias'.")
        return

    entity_id = content.get('id', content.get('alias', '').lower().replace(' ', '_'))
    if not entity_id:
        print_error(f"Could not determine entity ID for {filepath}")
        return

    # Determine if it's an automation or script
    is_automation = 'trigger' in content
    is_script = 'sequence' in content and not is_automation
    if not is_automation and not is_script:
        print(f"Skipping {filepath} as it does not appear to be an automation or script.")
        return
        
    entity_type = 'automation' if is_automation else 'script'
    api_path = f"/api/config/{entity_type}/config/{entity_id}"
    url = f"{ha_config['HA_URL']}{api_path}"
    headers = {"Authorization": f"Bearer {ha_config['HA_TOKEN']}", "Content-Type": "application/json"}

    # Check if entity exists
    try:
        resp = requests.get(url, headers=headers)
        exists = resp.status_code == 200

        if exists and not auto_overwrite:
            overwrite = input(f"'{entity_id}' already exists. Overwrite? [y/N] ").lower()
            if overwrite != 'y':
                print(f"Skipped {entity_id}.")
                return

        # Push the automation/script
        resp = requests.post(url, headers=headers, data=json.dumps(content))
        resp.raise_for_status()
        print(f"Successfully pushed {entity_type}: {entity_id}")

    except requests.exceptions.RequestException as e:
        print_error(f"Error pushing {entity_id}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Push Home Assistant automations/scripts.")
    parser.add_argument('--push-file', type=str, help='Push a single automation/script YAML file.')
    parser.add_argument('--auto-overwrite', action='store_true', help='Auto-accept all confirmation prompts.')
    parser.add_argument('--auto-detect-changes', action='store_true', help='Automatically push all changed YAML files since the last git commit.')
    args = parser.parse_args()

    global AUTO_OVERWRITE
    AUTO_OVERWRITE = args.auto_overwrite

    try:
        ha_config = get_config()
    except FileNotFoundError as e:
        print_error(e)
        return

    files_to_push = []
    if args.auto_detect_changes:
        files_to_push = get_changed_yaml_files()
    elif args.push_file:
        files_to_push.append(args.push_file)
    else:
        # Default behavior: push all files from configured directories
        automations_dir = ha_config.get('AUTOMATIONS_DIR')
        scripts_dir = ha_config.get('SCRIPTS_DIR')
        if automations_dir:
            files_to_push.extend(glob.glob(os.path.join(automations_dir, '*.yaml')))
        if scripts_dir:
            files_to_push.extend(glob.glob(os.path.join(scripts_dir, '*.yaml')))

    if not files_to_push:
        print("No files to push.")
        return

    for f in files_to_push:
        push_file(f, ha_config, auto_overwrite=AUTO_OVERWRITE)

if __name__ == "__main__":
    main()
