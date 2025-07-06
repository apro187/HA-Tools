#!/usr/bin/env python3
"""
pull_automations.py

Pulls the latest automations and scripts from a Home Assistant instance
and saves them to the configured local directories.
"""
from ha_helpers.common import get_config, pull_and_save_ha_items

def main():
    """Main function to pull automations and scripts."""
    try:
        config = get_config()
        ha_url = config['HA_URL']
        ha_token = config['HA_TOKEN']
        automations_dir = config.get('AUTOMATIONS_DIR')
        scripts_dir = config.get('SCRIPTS_DIR')

        print("Pulling automations and scripts from Home Assistant...")
        if automations_dir:
            pull_and_save_ha_items('automation', '/api/config/automation/config', automations_dir, ha_url, ha_token)
        if scripts_dir:
            pull_and_save_ha_items('script', '/api/config/script/config', scripts_dir, ha_url, ha_token)
        print("\nPull complete!")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
