# automation_watchdog.py

## Overview
Watches Home Assistant automations in real time and reports failures using the WebSocket API.

## Usage

```bash
automation-watchdog [OPTIONS]
```

| Option         | Type   | Default    | Description                                 |
|----------------|--------|------------|---------------------------------------------|
| `--ha-path`    | str    | (required) | Path to your Home Assistant config directory |
| `--timeout`    | float  | 3          | Seconds to wait before fetching trace        |
| `--include`    | str    | (optional) | Comma-separated list of automations to watch |
| `--exclude`    | str    | (optional) | Comma-separated list of automations to ignore|

> Tip: run `automation-watchdog --help` to see the full list.

## Example


```bash
automation-watchdog --ha-path ~/ha-config --timeout 5 --include automation.kitchen_lights
```

### Sample output

```
★ Watchdog running…  (Ctrl-C to quit)
✖  automation.kitchen_lights failed after 120 ms  (run 1234abc)
```

## Home Assistant automation/snippet

```yaml
alias: Watchdog notification
mode: single
trigger:
  - platform: state
    entity_id: automation.kitchen_lights
    to: 'off'
action:
  - service: notify.mobile_app
    data:
      message: 'Kitchen lights automation failed!'
```

## Troubleshooting

| Error                  | Hint                                 |
|------------------------|--------------------------------------|
| WebSocket auth failed  | Check your HA token in config.json    |
| No events received     | Trigger an automation manually        |

---

## Changelog
- **v0.1** – initial version
