# generate_entity_state_doc.py

## Overview
Generates documentation for observed Home Assistant entity states based on ha_entities.json. Useful for auditing, refactoring, or documenting custom/unknown states.

## Usage

```bash
generate-entity-state-doc [OPTIONS]
```

| Option              | Type   | Default    | Description                                 |
|---------------------|--------|------------|---------------------------------------------|
| `--ha-path`         | str    | (required) | Path to your Home Assistant config directory |
| `--automations-dir` | str    | (optional) | Path to your automations YAML folder         |
| `--scripts-dir`     | str    | (optional) | Path to your scripts YAML folder             |

> Tip: run `generate-entity-state-doc --help` to see the full list.

## Example


```bash
generate-entity-state-doc --ha-path ~/ha-config
```

### Sample output

```
Wrote entity state documentation to entity_states.json
Found custom/unknown states for 3 entities.
```

## Home Assistant automation/snippet

```yaml
alias: Generate entity state doc
mode: single
trigger:
  - platform: time
    at: '04:00:00'
action:
  - service: python_script.generate_entity_state_doc
```

## Troubleshooting

| Error                        | Hint                                 |
|------------------------------|--------------------------------------|
| ha_entities.json not found   | Run get_ha_entities.py first          |
| Error decoding JSON          | Check ha_entities.json for corruption |

---

## Changelog
- **v0.1** – initial version
