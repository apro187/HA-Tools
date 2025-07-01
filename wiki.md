# Home Assistant Tools (ha-tools) Wiki

Welcome to the ha-tools documentation! This wiki covers setup, configuration, and usage for all included scripts.

---

## Table of Contents
- [Setup & Configuration](#setup--configuration)
- [Folder Structure](#folder-structure)
- [Script Reference](#script-reference)
  - [push_automation.py](#push_automationpy)
  - [automation_watchdog.py](#automation_watchdogpy)
  - [get_ha_entities.py](#get_ha_entitiespy)
  - [get_recent_trace_errors.py](#get_recent_trace_errorspy)
  - [generate_entity_state_doc.py](#generate_entity_state_docpy)
  - [setup_ha_tools.py](#setup_ha_toolspy)

---

## Setup & Configuration

1. **Run the interactive setup:**
   ```sh
   python src/setup_ha_tools.py
   ```
   - Prompts for your Home Assistant URL, API token, and preferred directories for config, automations, and scripts.
   - Stores secrets/config in a hidden `.ha-tools-config/config.json` folder in the parent directory of your automations/scripts (never in the project folder).
   - You can override the config location by setting the `HA_TOOLS_CONFIG_BASE` environment variable.
   - The setup script will display the exact config path after setup.
   - Creates a default folder structure in `~/Documents/HA-Tools-Data` if you don't specify custom locations.
   - Validates your Home Assistant connection and token before saving.

2. **Install requirements:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configuration is stored at:**
   - By default: `.ha-tools-config/config.json` in the parent directory of your automations/scripts
   - Or as set by the `HA_TOOLS_CONFIG_BASE` environment variable
   - Never in the repo/project folder

---

## Folder Structure

- `src/` — All CLI tool scripts
- `README.md`, `setup.py`, `requirements.txt` — Project metadata and dependencies
- User config/secrets are **never** stored in the repo folder

Default data folders (can be customized):
- `~/Documents/HA-Tools-Data/config` — config files
- `~/Documents/HA-Tools-Data/automations` — automations YAML
- `~/Documents/HA-Tools-Data/scripts` — scripts YAML

---

## Script Reference

### push_automation.py
Pushes Home Assistant automations and scripts to your HA instance via the REST API.

**Usage:**
```sh
python src/push_automation.py --ha-path <HA_CONFIG_PATH> [--automations-dir <DIR>] [--scripts-dir <DIR>] [--push-file <YAML_FILE>] [--auto-overwrite]
```

**Arguments:**
- `--ha-path <HA_CONFIG_PATH>`: Path to the Home Assistant config directory (required)
- `--automations-dir <DIR>`: Path to your automations YAML folder (optional)
- `--scripts-dir <DIR>`: Path to your scripts YAML folder (optional)
- `--push-file <YAML_FILE>`: Push a single automation/script YAML file
- `--auto-overwrite`: Auto-accept all confirmation prompts

**Features:**
- Push all or individual YAML files
- Lint YAML before pushing
- Auto-overwrite with confirmation or flag
- Custom folder mapping

---

### automation_watchdog.py
Watches Home Assistant automations in real time and reports failures using the WebSocket API.

**Usage:**
```sh
python src/automation_watchdog.py --ha-path <HA_CONFIG_PATH> [--timeout SECONDS] [--include a,b] [--exclude x,y]
```

**Arguments:**
- `--ha-path <HA_CONFIG_PATH>`: Path to the Home Assistant config directory (required)
- `--timeout SECONDS`: Seconds to wait before fetching trace (default: 3)
- `--include a,b`: Comma-separated list of automations to watch
- `--exclude x,y`: Comma-separated list of automations to ignore

**Features:**
- Real-time error reporting
- Filter by automation entity_id

---

### get_ha_entities.py
Fetches all Home Assistant entities and their states via the REST API and writes them to ha_entities.json.

**Usage:**
```sh
python src/get_ha_entities.py --ha-path <HA_CONFIG_PATH> [--automations-dir <DIR>] [--scripts-dir <DIR>]
```

**Arguments:**
- `--ha-path <HA_CONFIG_PATH>`: Path to the Home Assistant config directory (required)
- `--automations-dir <DIR>`: Path to your automations YAML folder (optional)
- `--scripts-dir <DIR>`: Path to your scripts YAML folder (optional)

**Features:**
- Fetches all entity states and attributes
- Saves to ha_entities.json for use by other tools

---

### get_recent_trace_errors.py
Fetches recent Home Assistant automation/script trace errors using the WebSocket API.

**Usage:**
```sh
python src/get_recent_trace_errors.py --ha-path <HA_CONFIG_PATH> [--minutes N] [--automations-dir <DIR>] [--scripts-dir <DIR>]
```

**Arguments:**
- `--ha-path <HA_CONFIG_PATH>`: Path to the Home Assistant config directory (required)
- `--minutes N`: How many minutes back to check for errors (default: 10)
- `--automations-dir <DIR>`: Path to your automations YAML folder (optional)
- `--scripts-dir <DIR>`: Path to your scripts YAML folder (optional)

**Features:**
- Reports errors found in the last N minutes
- Uses WebSocket API for trace data

---

### generate_entity_state_doc.py
Generates documentation for observed Home Assistant entity states based on ha_entities.json.

**Usage:**
```sh
python src/generate_entity_state_doc.py --ha-path <HA_CONFIG_PATH> [--automations-dir <DIR>] [--scripts-dir <DIR>]
```

**Arguments:**
- `--ha-path <HA_CONFIG_PATH>`: Path to the Home Assistant config directory (required)
- `--automations-dir <DIR>`: Path to your automations YAML folder (optional)
- `--scripts-dir <DIR>`: Path to your scripts YAML folder (optional)

**Features:**
- Compares observed states to known domain states
- Outputs custom/unknown states by entity and domain

---

### setup_ha_tools.py
Interactive setup script for ha-tools. Prompts for Home Assistant URL, API token, and local automations/scripts directories.

**Usage:**
```sh
python src/setup_ha_tools.py
```

**Features:**
- Prompts for all required info
- Validates connection and token
- Creates default folders if needed
- Stores config securely in a hidden `.ha-tools-config` folder in the parent directory of your automations/scripts (never in the project folder)
- You can override the config location with the `HA_TOOLS_CONFIG_BASE` environment variable

---

## FAQ
- **Where are my secrets/config stored?**
  - By default, in `.ha-tools-config/config.json` in the parent directory of your automations/scripts (never in the project folder).
  - You can override this location with the `HA_TOOLS_CONFIG_BASE` environment variable.
- **How do I update my config?**
  - Re-run `python src/setup_ha_tools.py` at any time.
- **How do I contribute?**
  - Fork the repo, make changes, and submit a pull request!

---

For more, see the [README.md](../README.md) or open an issue on GitHub.
