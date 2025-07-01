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
1. Place your Home Assistant `ha_config.json` (with `HA_URL` and `HA_TOKEN`) in your HA config directory.
2. Use the `--ha-path` argument (or set the `HA_CONFIG_PATH` environment variable) to specify the path to your HA config directory for all tools.
3. Optionally, use `--automations-dir` and/or `--scripts-dir` to map your local automations/scripts folders if they are not in the standard Home Assistant locations.

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

## License
MIT
