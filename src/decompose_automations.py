utomations#!/usr/bin/env python3
"""
decompose_automations.py

Decomposes a Home Assistant automations.yaml or scripts.yaml file into individual YAML files.

Usage:
  python decompose_automations.py --ha-path <HA_CONFIG_PATH> --file <FILE_TO_DECOMPOSE> --output-dir <OUTPUT_DIRECTORY>

Arguments:
  --ha-path <HA_CONFIG_PATH>   Path to the Home Assistant config directory (required)
  --file <FILE_TO_DECOMPOSE>   Path to the automations.yaml or scripts.yaml file to decompose
  --output-dir <OUTPUT_DIR>    The directory to output the individual YAML files to.
"""
import os
import argparse
import yaml
import json

def print_error(msg):
    """Prints an error message to the console."""
    print(f"\033[91m{msg}\033[0m")

def load_ha_config(ha_path):
    """Loads the Home Assistant configuration from config.json."""
    default_config = os.path.expanduser('~/Documents/HA-Tools/config/config.json')
    config_path = os.path.join(ha_path, 'config.json') if os.path.exists(os.path.join(ha_path, 'config.json')) else default_config
    if not os.path.exists(config_path):
        print_error(f"Configuration file not found at: {config_path}")
        return None
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    """Main function to decompose automations or scripts."""
    parser = argparse.ArgumentParser(description="Decompose Home Assistant automations or scripts into individual files.")
    parser = argparse.ArgumentParser(description="Decompose Home Assistant automations or scripts into individual files.")
    parser.add_argument('--ha-path', type=str, default=os.path.expanduser('~/Documents/HA-Tools/config'),
                        help='Path to Home Assistant config directory (default: ~/Documents/HA-Tools/config)')
    parser.add_argument('--file', type=str,
                        help='Path to the automations.yaml or scripts.yaml file to decompose.')
    parser.add_argument('--output-dir', type=str,
                        help='The directory to output the individual YAML files to.')
    args = parser.parse_args()

    ha_config = load_ha_config(args.ha_path)
    if not ha_config:
        exit(1)

    # Auto-detect file and output-dir if not provided
    if not args.file or not args.output_dir:
        automations_dir = ha_config.get('AUTOMATIONS_DIR') or os.path.expanduser('~/Documents/HA-Tools/automations')
        scripts_dir = ha_config.get('SCRIPTS_DIR') or os.path.expanduser('~/Documents/HA-Tools/scripts')
        ha_path = args.ha_path
        # Prefer automations.yaml if present, else scripts.yaml
        if not args.file:
            auto_file = None
            if automations_dir and os.path.exists(os.path.join(automations_dir, 'automations.yaml')):
                auto_file = os.path.join(automations_dir, 'automations.yaml')
            elif scripts_dir and os.path.exists(os.path.join(scripts_dir, 'scripts.yaml')):
                auto_file = os.path.join(scripts_dir, 'scripts.yaml')
            elif os.path.exists(os.path.join(ha_path, 'automations.yaml')):
                auto_file = os.path.join(ha_path, 'automations.yaml')
            elif os.path.exists(os.path.join(ha_path, 'scripts.yaml')):
                auto_file = os.path.join(ha_path, 'scripts.yaml')
            if not auto_file:
                print_error('Could not auto-detect automations.yaml or scripts.yaml. Please specify --file.')
                exit(1)
            args.file = auto_file
            print(f"Auto-detected file: {args.file}")
        if not args.output_dir:
            if 'automations' in os.path.basename(args.file):
                args.output_dir = automations_dir
            elif 'scripts' in os.path.basename(args.file):
                args.output_dir = scripts_dir
            else:
                args.output_dir = os.path.join(ha_path, 'decomposed')
            print(f"Auto-detected output directory: {args.output_dir}")
    # Load the YAML file
    try:
        with open(args.file, 'r') as f:
            docs = list(yaml.safe_load_all(f))
    except Exception as e:
        print_error(f"Failed to load YAML: {e}")
        exit(1)

    # If the YAML is a list, treat each item as an automation/script
    if isinstance(docs, list) and len(docs) == 1 and isinstance(docs[0], list):
        items = docs[0]
    else:
        items = docs

    if not isinstance(items, list):
        print_error("YAML file does not contain a list of automations/scripts.")
        exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    for idx, item in enumerate(items):
        # Use alias or id for filename if available
        name = item.get('alias') or item.get('id') or f'item_{idx+1}'
        # Sanitize filename
        safe_name = ''.join(c if c.isalnum() or c in ('-', '_') else '_' for c in str(name))
        out_path = os.path.join(args.output_dir, f'{safe_name}.yaml')
        try:
            with open(out_path, 'w') as out_f:
                yaml.safe_dump([item], out_f, sort_keys=False, allow_unicode=True)
            print(f"Wrote: {out_path}")
        except Exception as e:
            print_error(f"Failed to write {out_path}: {e}")

if __name__ == '__main__':
    main()
