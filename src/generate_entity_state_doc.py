"""
generate_entity_state_doc.py

Generates documentation for observed Home Assistant entity states based on ha_entities.json.

- Scans all entities and their states from ha_entities.json.
- Compares observed states to known domain states.
- Outputs a JSON file listing custom/unknown states by entity and domain.

Usage:
  python generate_entity_state_doc.py --ha-path <HA_CONFIG_PATH> [--automations-dir <DIR>] [--scripts-dir <DIR>]

Arguments:
  --ha-path <HA_CONFIG_PATH>   Path to the Home Assistant config directory (required)
  --automations-dir <DIR>      Path to your automations YAML folder (optional)
  --scripts-dir <DIR>          Path to your scripts YAML folder (optional)

Requires: ha_entities.json (run get_ha_entities.py first)
"""

import json
import os
from collections import defaultdict
import sys
import argparse

# Load entities from ha_entities.json

def load_entities(ha_path, scripts_dir=None, automations_dir=None):
    # Prefer user-specified scripts_dir/automations_dir if provided
    paths = []
    if automations_dir:
        paths.append(os.path.join(automations_dir, 'ha_entities.json'))
    if scripts_dir:
        paths.append(os.path.join(scripts_dir, 'ha_entities.json'))
    paths.append(os.path.join(ha_path, 'ha_entities.json'))
    for entities_path in paths:
        if os.path.exists(entities_path):
            with open(entities_path, 'r') as f:
                return json.load(f)
    print("ha_entities.json not found. Run get_ha_entities.py first.")
    exit(1)

# ...existing code...
# Add argparse for ha_path
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate documentation for Home Assistant entity states.")
    parser.add_argument('--ha-path', type=str, default=os.environ.get('HA_CONFIG_PATH'),
                        help='Path to Home Assistant config directory (required)')
    parser.add_argument('--automations-dir', type=str, help='Path to your automations YAML folder (optional)')
    parser.add_argument('--scripts-dir', type=str, help='Path to your scripts YAML folder (optional)')
    args = parser.parse_args()
    if not args.ha_path:
        print('You must specify --ha-path or set the HA_CONFIG_PATH environment variable.')
        exit(1)
    entities = load_entities(args.ha_path, scripts_dir=args.scripts_dir, automations_dir=args.automations_dir)
    # ...rest of script unchanged...
