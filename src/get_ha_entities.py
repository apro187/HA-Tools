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
    # Prefer config.json in ~/Documents/HA-Tools/config/config.json
    default_config = os.path.expanduser('~/Documents/HA-Tools/config/config.json')
    config_path = os.path.join(ha_path, 'config.json') if os.path.exists(os.path.join(ha_path, 'config.json')) else default_config
    if not os.path.exists(config_path):
        print('config.json not found.')
        exit(1)
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Fetch Home Assistant entities and states via REST API.")
    parser.add_argument('--ha-path', type=str, default=os.path.expanduser('~/Documents/HA-Tools/config'),
                        help='Path to Home Assistant config directory (default: ~/Documents/HA-Tools/config)')
    parser.add_argument('--automations-dir', type=str, help='Path to your automations YAML folder (optional)')
    parser.add_argument('--scripts-dir', type=str, help='Path to your scripts YAML folder (optional)')
    args = parser.parse_args()
    config = load_ha_config(args.ha_path, automations_dir=args.automations_dir, scripts_dir=args.scripts_dir)
    HA_URL = config['HA_URL']
    HA_TOKEN = config['HA_TOKEN']
    automations_dir = args.automations_dir or config.get('AUTOMATIONS_DIR') or os.path.expanduser('~/Documents/HA-Tools/automations')
    scripts_dir = args.scripts_dir or config.get('SCRIPTS_DIR') or os.path.expanduser('~/Documents/HA-Tools/scripts')
    # Save ha_entities.json in config folder by default
    entities_path = os.path.join(args.ha_path, 'ha_entities.json')
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(f"{HA_URL}/api/states", headers=headers)
        response.raise_for_status()
        entities = response.json()
        with open(entities_path, 'w') as temp_file:
            json.dump(entities, temp_file, indent=2)
        print(f"Home Assistant Entities and States (also saved to {entities_path}):")
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
