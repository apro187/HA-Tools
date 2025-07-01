# ha-tools

A collection of Python command-line tools for Home Assistant automation management and diagnostics.

## Features
- Push automations/scripts to Home Assistant with CLI
- Fetch and analyze trace errors
- Watchdog for automation health
- Designed for cross-platform use (macOS/Linux/Windows)

## Usage

All tools are in the `src/` directory. Each tool supports `--help` for CLI options.

**Setup:**
1. Run the interactive setup script:
   ```sh
   python src/setup_ha_tools.py
   ```
   - Prompts for your Home Assistant URL, API token, and preferred directories for config, automations, and scripts.
   - Stores secrets/config in a hidden `.ha-tools-config/config.json` folder in the parent directory of your automations/scripts (never in the project folder).
   - You can override the config location by setting the `HA_TOOLS_CONFIG_BASE` environment variable.
   - The setup script will display the exact config path after setup.

2. Install requirements:
   ```sh
   pip install -r requirements.txt
   ```

3. **Configuration is stored at:**
   - By default: `.ha-tools-config/config.json` in the parent directory of your automations/scripts
   - Or as set by the `HA_TOOLS_CONFIG_BASE` environment variable
   - Never in the repo/project folder

**Example: Push all automations/scripts to Home Assistant**

```sh
python src/push_automation.py --ha-path /path/to/your/ha/config --automations-dir /path/to/your/automations --scripts-dir /path/to/your/scripts
```

- If you do not specify `--automations-dir` or `--scripts-dir`, the tool will look for `automations/` and `scripts/` subfolders under your `--ha-path`.
- You can also push a single file with `--push-file`.

**Example: Watch automations for failures**

```sh
python src/automation_watchdog.py --ha-path /path/to/your/ha/config --timeout 3
```

**Example: Fetch recent trace errors**

```sh
python src/get_recent_trace_errors.py --ha-path /path/to/your/ha/config --minutes 10
```

**Example: Generate entity state documentation**

```sh
python src/generate_entity_state_doc.py --ha-path /path/to/your/ha/config
```

**Example: Fetch all entities from Home Assistant**

```sh
python src/get_ha_entities.py --ha-path /path/to/your/ha/config
```

- `--ha-path` is required (or set the `HA_CONFIG_PATH` environment variable)
- See each tool's `--help` for more options

## Development
- Python 3.9+
- Install dependencies: `pip install -r requirements.txt`

## FAQ
- **Where are my secrets/config stored?**
  - By default, in `.ha-tools-config/config.json` in the parent directory of your automations/scripts (never in the project folder).
  - You can override this location with the `HA_TOOLS_CONFIG_BASE` environment variable.
- **How do I update my config?**
  - Re-run `python src/setup_ha_tools.py` at any time.
- **How do I contribute?**
  - Fork the repo, make changes, and submit a pull request!

## License
MIT
