# pull_automations.py

## Overview
Pulls the latest automations and scripts from a Home Assistant instance and saves them to the configured local directories.

## Usage
```bash
pull-automations
```

This command takes no arguments. It uses the configuration from `~/Documents/HA-Tools/config/config.json` to connect to your Home Assistant instance.

## Example

```bash
pull-automations
```

### Sample output

```
Pulling automations and scripts from Home Assistant...
Pulled and saved 5 automation(s) to /Users/adamprostrollo/Documents/HA-Tools/automations
Pulled and saved 2 script(s) to /Users/adamprostrollo/Documents/HA-Tools/scripts

Pull complete!
```

## Home Assistant automation/snippet
This script is intended to be run from the command line and not as a Home Assistant service.

## Troubleshooting
| Error                                     | Hint                                                                      |
| ----------------------------------------- | ------------------------------------------------------------------------- |
| `Config file not found...`                | Run `setup-ha-tools` first to create the configuration file.              |
| `Error pulling automations...`            | Check your Home Assistant URL and token in the configuration file.        |
