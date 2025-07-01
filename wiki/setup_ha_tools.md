# setup_ha_tools.py

## Overview
Interactive setup script for ha-tools. Prompts for Home Assistant URL, API token, and local automations/scripts directories, and writes config securely.

## Usage
```bash
python src/setup_ha_tools.py
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| (none) |      |         | Interactive prompts for all fields |

> Tip: Run this script any time you want to update your config or change directories.

## Example

```bash
python src/setup_ha_tools.py
```

### Sample output

```
=== ha-tools Environment Setup ===
Found existing ha-tools config at /Users/you/.ha-tools-config/config.json.
Setup complete! You can now use ha-tools with your configuration.
```

## Home Assistant automation/snippet

```yaml
# Not applicable (setup script)
```

## Troubleshooting

| Error | Hint |
|-------|------|
| Could not connect to Home Assistant | Check your HA URL and network |
| Token is invalid or expired | Create a new long-lived access token in HA |

---

## Changelog
- **v0.1** – initial version
