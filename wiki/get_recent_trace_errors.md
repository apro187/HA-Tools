# get_recent_trace_errors.py

## Overview
Fetches recent Home Assistant automation/script trace errors using the WebSocket API.

## Usage
```bash
python src/get_recent_trace_errors.py [OPTIONS]
```

| Option              | Type   | Default    | Description                                 |
|---------------------|--------|------------|---------------------------------------------|
| `--ha-path`         | str    | (required) | Path to your Home Assistant config directory |
| `--minutes`         | int    | 10         | How many minutes back to check for errors    |
| `--automations-dir` | str    | (optional) | Path to your automations YAML folder         |
| `--scripts-dir`     | str    | (optional) | Path to your scripts YAML folder             |

> Tip: run `python src/get_recent_trace_errors.py --help` to see the full list.

## Example

```bash
python src/get_recent_trace_errors.py --ha-path ~/ha-config --minutes 30
```

### Sample output

```
Checking for traces with errors in the last 30 minutes...
Found 2 traces with errors:
[2025-06-30T12:34:56Z] automation.kitchen_lights trace_id=1234abc
  Error: Some error message
```

## Home Assistant automation/snippet

```yaml
alias: Nightly trace error report
mode: single
trigger:
  - platform: time
    at: '02:00:00'
action:
  - service: python_script.get_recent_trace_errors
```

## Troubleshooting

| Error                  | Hint                                 |
|------------------------|--------------------------------------|
| ha_config.json not found| Run setup_ha_tools.py first           |
| WebSocket auth failed  | Check your HA token in config.json    |

---

## Changelog
- **v0.1** – initial version
