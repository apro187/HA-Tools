# get_ha_entities.py

## Overview
Fetches all Home Assistant entities and their states via the REST API and writes them to ha_entities.json.

## Usage
```bash
python src/get_ha_entities.py [OPTIONS]
```

| Option              | Type   | Default    | Description                                 |
|---------------------|--------|------------|---------------------------------------------|
| `--ha-path`         | str    | (required) | Path to your Home Assistant config directory |
| `--automations-dir` | str    | (optional) | Path to your automations YAML folder         |
| `--scripts-dir`     | str    | (optional) | Path to your scripts YAML folder             |

> Tip: run `python src/get_ha_entities.py --help` to see the full list.

## Example

```bash
python src/get_ha_entities.py --ha-path ~/ha-config
```

### Sample output

```
Home Assistant Entities and States (also saved to /path/to/ha_entities.json):
------------------------------------
Entity ID: light.kitchen
State: on
--------------------
...etc...
```

## Home Assistant automation/snippet

```yaml
alias: Refresh entity list
mode: single
trigger:
  - platform: time
    at: '03:00:00'
action:
  - service: python_script.get_ha_entities
```

## Troubleshooting

| Error                        | Hint                                 |
|------------------------------|--------------------------------------|
| ha_config.json not found     | Run setup_ha_tools.py first           |
| Error communicating with API | Check your HA URL/token in config     |

---

## Changelog
- **v0.1** – initial version
