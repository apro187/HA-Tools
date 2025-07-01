#!/usr/bin/env python3
"""
setup_ha_tools.py

Interactive setup script for ha-tools. Prompts for Home Assistant URL, API token, and local automations/scripts directories.
Creates a config file in the user's config directory (never in the project folder).
"""
import os
import json
import sys
from urllib.parse import urlparse
import requests
import platform

# Prompt the user for input, with optional default and required flag
def prompt(msg, default=None, required=True):
    while True:
        val = input(f"{msg} " + (f"[{default}] " if default else "")).strip()
        if not val and default is not None:
            val = default
        if val or not required:
            return val
        print("This field is required.")

# Check if the Home Assistant URL is reachable
def check_ha_url(ha_url):
    try:
        resp = requests.get(ha_url)
        return resp.status_code == 200
    except Exception:
        return False

# Check if the Home Assistant token is valid
def check_ha_token(ha_url, ha_token):
    try:
        headers = {"Authorization": f"Bearer {ha_token}", "Content-Type": "application/json"}
        resp = requests.get(f"{ha_url}/api/states", headers=headers, timeout=10)
        return resp.status_code == 200
    except Exception:
        return False

# Get the default path for storing secrets/config (never in the project folder)
def get_default_secrets_path():
    # By default, store config in a hidden .ha-tools-config folder in the same parent as automations/scripts
    # Fallback to ~/.ha-tools-config/config.json if not set
    base = os.environ.get('HA_TOOLS_CONFIG_BASE')
    if not base:
        # Try to infer from default automations/scripts location
        _, config_dir, automations_dir, scripts_dir, logs_dir, prints_dir = get_default_folders()
        # Use config_dir for config
        base = config_dir
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, 'config.json')

# Get the default folder structure for config, automations, scripts, logs, and prints

def get_default_folders():
    base = os.path.expanduser('~/Documents/HA-Tools')
    config = os.path.join(base, 'config')
    automations = os.path.join(base, 'automations')
    scripts = os.path.join(base, 'scripts')
    logs = os.path.join(base, 'logs')
    prints = config  # Prints go directly in the config folder
    return base, config, automations, scripts, logs, prints

# Main interactive setup logic

def main():
    print("\n=== ha-tools Environment Setup ===\n")
    # Determine where to store the config/secrets
    base, config_dir, automations_dir, scripts_dir, logs_dir, prints_dir = get_default_folders()
    secrets_path = os.path.join(config_dir, 'config.json')
    # Create all folders if they don't exist
    for d in [base, config_dir, automations_dir, scripts_dir, logs_dir, prints_dir]:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
            print(f"Created directory: {d}")
    prev_config = None
    # Load previous config if it exists
    if os.path.exists(secrets_path):
        with open(secrets_path, 'r') as f:
            prev_config = json.load(f)
        print(f"Found existing ha-tools config at {secrets_path}.")
    # Prompt for config, automations, and scripts directories (use previous or default)
    ha_path = prompt("Path to your Home Assistant config directory:", default=prev_config.get('HA_PATH', config_dir) if prev_config else config_dir)
    automations_dir = prompt("Path to your automations directory (leave blank for default):", default=prev_config.get('AUTOMATIONS_DIR', automations_dir) if prev_config else automations_dir, required=False)
    scripts_dir = prompt("Path to your scripts directory (leave blank for default):", default=prev_config.get('SCRIPTS_DIR', scripts_dir) if prev_config else scripts_dir, required=False)
    logs_dir = prompt("Path to your logs directory (leave blank for default):", default=prev_config.get('LOGS_DIR', logs_dir) if prev_config else logs_dir, required=False)
    prints_dir = prompt("Path to your prints directory (leave blank for default):", default=prev_config.get('PRINTS_DIR', prints_dir) if prev_config else prints_dir, required=False)
    # Create folders if they don't exist
    for d in [ha_path, automations_dir, scripts_dir, logs_dir, prints_dir]:
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
            print(f"Created directory: {d}")
    # Prompt for Home Assistant URL and token, with option to keep previous
    if prev_config:
        if prompt("Keep previous Home Assistant URL?", default=prev_config.get('HA_URL'), required=False) in ['', 'y', 'Y', 'yes', None]:
            ha_url = prev_config['HA_URL']
        else:
            ha_url = prompt("Enter the URL for your Home Assistant instance (e.g. http://homeassistant.local:8123):", default=prev_config['HA_URL'])
        if prompt("Keep previous API token?", default='yes', required=False) in ['', 'y', 'Y', 'yes', None]:
            ha_token = prev_config['HA_TOKEN']
        else:
            print("\nTo use ha-tools, you need a Home Assistant Long-Lived Access Token.")
            parsed = urlparse(ha_url)
            api_link = f"{parsed.scheme}://{parsed.netloc}/profile/security"
            print(f"1. Open this link in your browser: {api_link}")
            print("2. Scroll down to 'Long-Lived Access Tokens' and create a new token.")
            print("3. Copy and paste the token below.")
            ha_token = prompt("Paste your Home Assistant Long-Lived Access Token:")
    else:
        ha_url = prompt("Enter the URL for your Home Assistant instance (e.g. http://homeassistant.local:8123):")
        if not ha_url.startswith("http"):
            ha_url = "http://" + ha_url
        ha_url = ha_url.rstrip('/')
        parsed = urlparse(ha_url)
        api_link = f"{parsed.scheme}://{parsed.netloc}/profile/security"
        print("\nTo use ha-tools, you need a Home Assistant Long-Lived Access Token.")
        print(f"1. Open this link in your browser: {api_link}")
        print("2. Scroll down to 'Long-Lived Access Tokens' and create a new token.")
        print("3. Copy and paste the token below.")
        ha_token = prompt("Paste your Home Assistant Long-Lived Access Token:")
    # Validate HA URL (loop until valid)
    while not check_ha_url(ha_url):
        print("Could not connect to Home Assistant at that URL. Please check and try again.")
        ha_url = prompt("Enter the URL for your Home Assistant instance:")
        parsed = urlparse(ha_url)
        api_link = f"{parsed.scheme}://{parsed.netloc}/profile/security"
    # Validate token (loop until valid)
    while not check_ha_token(ha_url, ha_token):
        print("Token is invalid or expired. Please create a new one.")
        parsed = urlparse(ha_url)
        api_link = f"{parsed.scheme}://{parsed.netloc}/profile/security"
        print(f"Open this link in your browser: {api_link}")
        ha_token = prompt("Paste your Home Assistant Long-Lived Access Token:")
    # Save config to user config directory (never in project folder)
    config = {
        "HA_URL": ha_url,
        "HA_TOKEN": ha_token,
        "HA_PATH": ha_path,
        "AUTOMATIONS_DIR": automations_dir,
        "SCRIPTS_DIR": scripts_dir,
        "LOGS_DIR": logs_dir,
        "PRINTS_DIR": prints_dir
    }
    with open(secrets_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"\nha-tools config written to {secrets_path}")
    if automations_dir:
        print(f"Automations directory: {automations_dir}")
    if scripts_dir:
        print(f"Scripts directory: {scripts_dir}")
    if logs_dir:
        print(f"Logs directory: {logs_dir}")
    if prints_dir:
        print(f"Prints directory: {prints_dir}")

    # --- Initial Pull of Automations and Scripts from Home Assistant ---
    import requests
    def pull_and_save_ha_items(item_type, api_path, save_dir):
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
                    import yaml
                    with open(fpath, 'w') as f:
                        yaml.dump(item, f, default_flow_style=False, allow_unicode=True)
                    count += 1
                except Exception as e:
                    print(f"Failed to save {item_type} {entity_id}: {e}")
            print(f"Pulled and saved {count} {item_type}(s) to {save_dir}")
        except Exception as e:
            print(f"Error pulling {item_type}s from Home Assistant: {e}")

    print("\nPulling automations and scripts from Home Assistant...")
    pull_and_save_ha_items('automation', '/api/config/automation/config', automations_dir)
    pull_and_save_ha_items('script', '/api/config/script/config', scripts_dir)

    print("\nSetup complete! You can now use ha-tools with your configuration.")
    print("\nExample usage:")
    print(f"  push-automation --ha-path '{ha_path}'" + (f" --automations-dir '{automations_dir}'" if automations_dir else "") + (f" --scripts-dir '{scripts_dir}'" if scripts_dir else ""))

if __name__ == "__main__":
    main()
