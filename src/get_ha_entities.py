"""
get_ha_entities.py

Fetches all Home Assistant entities and their states via the REST API and writes them to ha_entities.json.

- Connects to your Home Assistant instance using the REST API.
- Retrieves all entity states and attributes.
- Saves the result to ha_entities.json for use by other tools.

Usage:
  python get_ha_entities.py --ha-path <HA_CONFIG_PATH> [--automations-dir <DIR>] [--scripts-dir <DIR>]


Arguments:
  --ha-path <HA_CONFIG_PATH>   Path to the Home Assistant config directory (required)
  --automations-dir <DIR>      Path to your automations YAML folder (optional)
  --scripts-dir <DIR>          Path to your scripts YAML folder (optional)

Requires: requests
"""

import requests
import json
import os
import argparse

def load_ha_config(ha_path, automations_dir=None, scripts_dir=None):
    # Prefer user-specified automations_dir/scripts_dir if provided
    paths = []
    if automations_dir:
        paths.append(os.path.join(automations_dir, 'ha_config.json'))
    if scripts_dir:
        paths.append(os.path.join(scripts_dir, 'ha_config.json'))
    paths.append(os.path.join(ha_path, 'ha_config.json'))
    for config_path in paths:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    print('ha_config.json not found.')
    exit(1)

def main():
    parser = argparse.ArgumentParser(description="Fetch Home Assistant entities and states via REST API.")
    parser.add_argument('--ha-path', type=str, default=os.environ.get('HA_CONFIG_PATH'),
                        help='Path to Home Assistant config directory (required)')
    parser.add_argument('--automations-dir', type=str, help='Path to your automations YAML folder (optional)')
    parser.add_argument('--scripts-dir', type=str, help='Path to your scripts YAML folder (optional)')
    args = parser.parse_args()
    if not args.ha_path:
        print('You must specify --ha-path or set the HA_CONFIG_PATH environment variable.')
        exit(1)
    config = load_ha_config(args.ha_path, automations_dir=args.automations_dir, scripts_dir=args.scripts_dir)
    HA_URL = config['HA_URL']
    HA_TOKEN = config['HA_TOKEN']
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(f"{HA_URL}/api/states", headers=headers)
        response.raise_for_status()
        entities = response.json()
        temp_path = os.path.join(args.ha_path, 'ha_entities.json')
        with open(temp_path, 'w') as temp_file:
            json.dump(entities, temp_file, indent=2)
        print(f"Home Assistant Entities and States (also saved to {temp_path}):")
        print("------------------------------------")
        for entity in entities:
            entity_id = entity.get("entity_id")
            state = entity.get("state")
            attributes = entity.get("attributes", {})
            print(f"Entity ID: {entity_id}")
            print(f"State: {state}")
            print("-" * 20)
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Home Assistant API: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response from Home Assistant API.")

if __name__ == "__main__":
    main()
