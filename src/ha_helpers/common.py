import os
import json
import requests
import yaml

# Get the path to the config file
def get_config_path():
    config_base = os.environ.get('HA_TOOLS_CONFIG_BASE', os.path.expanduser('~/Documents/HA-Tools/config'))
    return os.path.join(config_base, 'config.json')

# Get the default folder structure for config, automations, scripts, logs, and prints
def get_default_folders():
    base = os.path.expanduser('~/Documents/HA-Tools')
    config = os.path.join(base, 'config')
    automations = os.path.join(base, 'automations')
    scripts = os.path.join(base, 'scripts')
    logs = os.path.join(base, 'logs')
    prints = config  # Prints go directly in the config folder
    return base, config, automations, scripts, logs, prints

# Load the config file
def get_config():
    config_path = get_config_path()
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}. Please run setup-ha-tools first.")
    with open(config_path, 'r') as f:
        return json.load(f)

# Pull and save automations or scripts from Home Assistant
def pull_and_save_ha_items(item_type, api_path, save_dir, ha_url, ha_token):
    headers = {"Authorization": f"Bearer {ha_token}", "Content-Type": "application/json"}
    url = f"{ha_url}{api_path}"
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        items = resp.json()
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        count = 0
        for item in items:
            # Use the entity_id or id as filename
            entity_id = item.get('id') or item.get('entity_id') or f"{item_type}_{count}"
            # Clean filename
            fname = str(entity_id).replace('.', '_').replace(' ', '_') + ".yaml"
            fpath = os.path.join(save_dir, fname)
            # Save as YAML
            try:
                with open(fpath, 'w') as f:
                    yaml.dump(item, f, default_flow_style=False, allow_unicode=True)
                count += 1
            except Exception as e:
                print(f"Failed to save {item_type} {entity_id}: {e}")
        print(f"Pulled and saved {count} {item_type}(s) to {save_dir}")
    except Exception as e:
        print(f"Error pulling {item_type}s from Home Assistant: {e}")
