# ha-tools

A collection of Python command-line tools for Home Assistant automation management and diagnostics.

## Features
- Push automations/scripts to Home Assistant with CLI
- Pull automations/scripts from Home Assistant
- Fetch and analyze trace errors
- Watchdog for automation health
- Designed for cross-platform use (macOS/Linux/Windows)

## Getting Started

1.  **Prerequisites**:
    *   Python 3.9+
    *   Git
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/apro187/HA-Tools.git
    cd HA-Tools
    ```
3.  **Install the tools**:
    ```bash
    pip install .
    ```
4.  **Run the interactive setup**:
    ```bash
    setup-ha-tools
    ```

## Streamlined Workflow

The recommended workflow is to use Git to manage your automations and scripts:

1.  **Pull Changes from Home Assistant:**
    ```bash
    pull-automations
    ```
2.  **Commit the Pulled Changes:**
    ```bash
    git add .
    git commit -m "Sync automations from Home Assistant"
    ```
3.  **Edit Your Automations:**
    *   Make your desired changes to your automation and script files in your IDE.
4.  **Commit Your Changes:**
    ```bash
    git add .
    git commit -m "feat: add new thermostat automation"
    ```
5.  **Push Your Changes to Home Assistant:**
    ```bash
    push-automation --auto-detect-changes
    ```

## Usage

All tools are installed as CLI commands after running `pip install .` in this directory. Each tool supports `--help` for CLI options.

**Configuration is stored at:**
- By default: `config/config.json` in your `~/Documents/HA-Tools` directory
- Or as set by the `HA_TOOLS_CONFIG_BASE` environment variable
- Never in the repo/project folder

**Example: Push all automations/scripts to Home Assistant**


```sh
push-automation --auto-detect-changes
```

- The `--auto-detect-changes` flag will automatically find all YAML files that were part of the *last Git commit* and push them. **Ensure your changes are committed before using this flag.**
- You can also push all files in the configured directories by running `push-automation` without any flags.
- To push a single file, use `push-automation --push-file /path/to/your/file.yaml`.

**Example: Pull all automations/scripts from Home Assistant**

```sh
pull-automations
```
- This will pull all automations and scripts from your Home Assistant instance and save them to your configured local directories.

**Example: Watch automations for failures**


```sh
automation-watchdog --ha-path /path/to/your/ha/config --timeout 3
```

**Example: Fetch recent trace errors**


```sh
get-recent-trace-errors --ha-path /path/to/your/ha/config --minutes 10
```

**Example: Generate entity state documentation**


```sh
generate-entity-state-doc --ha-path /path/to/your/ha/config
```

**Example: Fetch all entities from Home Assistant**


```sh
get-ha-entities --ha-path /path/to/your/ha/config
```

- `--ha-path` is required (or set the `HA_CONFIG_PATH` environment variable)
- See each tool's `--help` for more options

## Development
- Python 3.9+
- Install dependencies: `pip install .` to install CLI tools

## FAQ
- **Where are my secrets/config stored?**
  - By default, in `config/config.json` in your `~/Documents/HA-Tools` directory (never in the project folder).
  - You can override this location with the `HA_TOOLS_CONFIG_BASE` environment variable.
  - The setup script also pulls all automations and scripts from your Home Assistant instance on first run.
- **How do I update my config?**
  - Re-run `setup-ha-tools` at any time.
- **How do I contribute?**
  - Fork the repo, make changes, and submit a pull request!

## License
MIT
