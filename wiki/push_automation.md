# push_automation.py

## Overview
Push a local YAML automation or script to Home Assistant via the REST API, with optional reload and linting.

## Usage

```bash
push-automation [OPTIONS]
```

| Option                | Type   | Default      | Description                                 |
|-----------------------|--------|--------------|---------------------------------------------|
| `--auto-detect-changes` | flag   | false        | Automatically push all YAML files that were part of the *last Git commit*. Requires changes to be committed first. |
| `--push-file`         | str    | (optional)   | Push a single automation/script YAML file    |
| `--auto-overwrite`    | flag   | false        | Auto-accept all confirmation prompts         |

> Tip: run `push-automation --help` to see the full list.

## Example


```bash
push-automation --auto-detect-changes
```

### Sample output

```
Pushed automation: my_automation.yaml
Pushed script: my_script.yaml
```

## Home Assistant automation/snippet

```yaml
alias: Push automation from CLI
mode: single
trigger:
  - platform: state
    entity_id: input_boolean.push_automation
    to: 'on'
action:
  - service: shell_command.push_automation
```

## Troubleshooting

| Error                | Hint                                 |
|----------------------|--------------------------------------|
| No YAML files found  | Check your automations/scripts paths  |
| 401 Unauthorized     | Check your HA token in config.json    |
| Not a git repository | Ensure you are running the script from within your private automations/scripts Git repository. |
| No new YAML files detected in the last commit. | Ensure you have committed your changes before running with `--auto-detect-changes`. |

---

## Changelog
- **v0.3** – Modified `--auto-detect-changes` to push only files from the last Git commit.
- **v0.2** – Added --auto-detect-changes flag
- **v0.1** – initial version
