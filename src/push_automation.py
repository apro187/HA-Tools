#!/usr/bin/env python3
"""
push_automation.py

Pushes Home Assistant automations and scripts to your HA instance via the REST API.

- Supports pushing all YAML files in automations/scripts folders, or a single file.
- Can auto-overwrite existing automations/scripts with confirmation or --auto-overwrite flag.
- Supports custom folder mapping for automations and scripts.
- Lints YAML before pushing and checks for existing entities.

Usage:
  python push_automation.py --ha-path <HA_CONFIG_PATH> [--automations-dir <DIR>] [--scripts-dir <DIR>] [--push-file <YAML_FILE>] [--auto-overwrite]

Arguments:
  --ha-path <HA_CONFIG_PATH>   Path to the Home Assistant config directory (required)
  --automations-dir <DIR>      Path to your automations YAML folder (optional)
  --scripts-dir <DIR>          Path to your scripts YAML folder (optional)
  --push-file <YAML_FILE>      Push a single automation/script YAML file
  --auto-overwrite             Auto-accept all confirmation prompts

Requires: requests, PyYAML
"""
import os
import glob
import yaml
import json
import requests
import re
from pathlib import Path
import argparse

# Global flag for auto-overwrite
AUTO_OVERWRITE = False

# Replace all hardcoded paths with ha_path argument

def print_error(msg):
    print(f"\033[91m{msg}\033[0m")

def get_automation_files(directory):
    return glob.glob(os.path.join(directory, '*.yaml'))

def get_yaml_files_from_dirs(dirs, automations_dir=None, scripts_dir=None):
    files = []
    for d in dirs:
        if os.path.isdir(d):
            # If user specifies automations_dir or scripts_dir, use those
            if automations_dir and os.path.abspath(d) == os.path.abspath(automations_dir):
                files.extend(glob.glob(os.path.join(d, '*.yaml')))
            elif scripts_dir and os.path.abspath(d) == os.path.abspath(scripts_dir):
                files.extend(glob.glob(os.path.join(d, '*.yaml')))
            else:
                # Standard Home Assistant: automations in 'automations', scripts in 'scripts'
                for sub in ['automations', 'automation', 'scripts']:
                    subdir = os.path.join(d, sub)
                    if os.path.isdir(subdir):
                        files.extend(glob.glob(os.path.join(subdir, '*.yaml')))
                # Also add any YAMLs in the folder itself
                files.extend(glob.glob(os.path.join(d, '*.yaml')))
        elif os.path.isfile(d) and d.endswith('.yaml'):
            files.append(d)
    return files

def load_ha_config(ha_path):
    # Look for config.json in ~/Documents/HA-Tools/config/config.json by default
    default_config = os.path.expanduser('~/Documents/HA-Tools/config/config.json')
    config_path = os.path.join(ha_path, 'config.json') if os.path.exists(os.path.join(ha_path, 'config.json')) else default_config
    if not os.path.exists(config_path):
        print_error(f"Config file not found at {config_path}")
        exit(1)
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Push Home Assistant automations/scripts to your HA instance.")
    parser.add_argument('--ha-path', type=str, default=os.path.expanduser('~/Documents/HA-Tools/config'),
                        help='Path to Home Assistant config directory (default: ~/Documents/HA-Tools/config)')
    parser.add_argument('--automations-dir', type=str, help='Path to your automations YAML folder (optional)')
    parser.add_argument('--scripts-dir', type=str, help='Path to your scripts YAML folder (optional)')
    parser.add_argument('--push-file', type=str, help='Push a single automation/script YAML file')
    parser.add_argument('--auto-overwrite', action='store_true', help='Auto-accept all confirmation prompts')
    args = parser.parse_args()

    global AUTO_OVERWRITE
    AUTO_OVERWRITE = args.auto_overwrite

    ha_path = args.ha_path
    ha_config = load_ha_config(ha_path)

    automations_dir = args.automations_dir or ha_config.get('AUTOMATIONS_DIR') or os.path.expanduser('~/Documents/HA-Tools/automations')
    scripts_dir = args.scripts_dir or ha_config.get('SCRIPTS_DIR') or os.path.expanduser('~/Documents/HA-Tools/scripts')

    if args.push_file:
        push_file_quiet(args.push_file, auto_overwrite=AUTO_OVERWRITE, ha_path=ha_path)
        return

    # Use automations_dir and scripts_dir as sources
    src_dirs = [automations_dir, scripts_dir]
    files = get_yaml_files_from_dirs(src_dirs, automations_dir=automations_dir, scripts_dir=scripts_dir)
    if not files:
        print_error("No YAML files found.")
        return

def push_file_quiet(filepath, auto_overwrite=False, ha_path=None):
    if not ha_path:
        ha_path = os.environ.get('HA_CONFIG_PATH')
    if not ha_path:
        print_error('You must specify --ha-path or set the HA_CONFIG_PATH environment variable.')
        exit(1)
    ha_config = load_ha_config(ha_path)
