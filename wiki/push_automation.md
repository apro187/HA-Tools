# push_automation.py

## Overview
Push a local YAML automation or script to Home Assistant via the REST API, with optional reload and linting.

## Usage

```bash
push-automation [OPTIONS]
```

| Option                | Type   | Default      | Description                                 |
|-----------------------|--------|--------------|---------------------------------------------|
| `--ha-path`           | str    | (required)   | Path to your Home Assistant config directory |
| `--automations-dir`   | str    | (optional)   | Path to your automations YAML folder         |
| `--scripts-dir`       | str    | (optional)   | Path to your scripts YAML folder             |
| `--push-file`         | str    | (optional)   | Push a single automation/script YAML file    |
| `--auto-overwrite`    | flag   | false        | Auto-accept all confirmation prompts         |

> Tip: run `push-automation --help` to see the full list.

## Example


```bash
push-automation --ha-path ~/ha-config --automations-dir ~/automations --scripts-dir ~/scripts --push-file my_automation.yaml --auto-overwrite
```

### Sample output

```
Pushed automation: my_automation.yaml
Reloaded automations.
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
  - service: python_script.push_automation
```

## Troubleshooting

| Error                | Hint                                 |
|----------------------|--------------------------------------|
| No YAML files found  | Check your automations/scripts paths  |
| 401 Unauthorized     | Check your HA token in config.json    |

---

## Changelog
- **v0.1** – initial version
