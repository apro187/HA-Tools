"""
get_recent_trace_errors.py

Fetches recent Home Assistant automation/script trace errors using the WebSocket API.

- Connects to your Home Assistant instance via WebSocket.
- Retrieves recent traces for automations and scripts.
- Reports errors found in the last N minutes.

Usage:
  python get_recent_trace_errors.py --ha-path <HA_CONFIG_PATH> [--minutes N] [--automations-dir <DIR>] [--scripts-dir <DIR>]

Arguments:
  --ha-path <HA_CONFIG_PATH>   Path to the Home Assistant config directory (required)
  --minutes N                  How many minutes back to check for errors (default: 10)
  --automations-dir <DIR>      Path to your automations YAML folder (optional)
  --scripts-dir <DIR>          Path to your scripts YAML folder (optional)

Requires: websockets, python-dateutil
"""

import json
import datetime
import asyncio
import websockets
import os
import argparse
from dateutil import parser, tz

def load_ha_config(ha_path, automations_dir=None, scripts_dir=None):
    # Prefer config.json in ~/Documents/HA-Tools/config/config.json
    default_config = os.path.expanduser('~/Documents/HA-Tools/config/config.json')
    config_path = os.path.join(ha_path, 'config.json') if os.path.exists(os.path.join(ha_path, 'config.json')) else default_config
    if not os.path.exists(config_path):
        print('config.json not found.')
        exit(1)
    with open(config_path, 'r') as f:
        return json.load(f)

async def get_trace(ws, domain: str, item_id: str, run_id: str) -> dict:
    await ws.send(json.dumps({
        "type": "trace/get",
        "domain": domain,
        "item_id": item_id,
        "run_id": run_id
    }))
    response = json.loads(await ws.recv())
    if not response.get("success"):
        print(f"Failed to fetch trace for {domain}.{item_id} (run {run_id[:7]})")
        return None
    return response.get("result", {}).get("trace", {})

async def get_traces_for_item(ws, domain: str, item_id: str) -> list:
    await ws.send(json.dumps({
        "type": "trace/list",
        "domain": domain,
        "item_id": item_id
    }))
    response = json.loads(await ws.recv())
    if not response.get("success"):
        print(f"Failed to list traces for {domain}.{item_id}")
        return []
    return response.get("result", [])

async def get_recent_traces(ws, domain: str, entity_id: str, minutes: int = 10) -> list:
    traces = await get_traces_for_item(ws, domain, entity_id)
    now = datetime.datetime.now(tz=tz.UTC)
    recent = []
    for trace_info in traces:
        run_id = trace_info.get("run_id")
        if not run_id:
            continue
        start = parser.isoparse(trace_info.get("timestamp", ""))
        if (now - start).total_seconds() > minutes * 60:
            continue
        trace = await get_trace(ws, domain, entity_id, run_id)
        if not trace:
            continue
        if trace.get("error"):
            recent.append({
                'trace_id': run_id,
                'timestamp': trace_info.get("timestamp"),
                'error': trace.get("error"),
                'domain': domain,
                'entity_id': entity_id
            })
    return recent

async def get_entities(ws, domain: str) -> list:
    await ws.send(json.dumps({
        "type": "config/entity_registry/list"
    }))
    response = json.loads(await ws.recv())
    if not response.get("success"):
        print(f"Failed to fetch entities")
        return []
    return [e["entity_id"].split(".", 1)[1] 
            for e in response.get("result", [])
            if e["entity_id"].startswith(f"{domain}.")]

async def main_async(ha_path, minutes=10, automations_dir=None, scripts_dir=None):
    ha_config = load_ha_config(ha_path, automations_dir=automations_dir, scripts_dir=scripts_dir)
    url = ha_config['HA_URL'].replace('https://', 'wss://').replace('http://', 'ws://')
    if not url.endswith('/api/websocket'):
        url = url.rstrip('/') + '/api/websocket'
    token = ha_config['HA_TOKEN']
    async with websockets.connect(url) as ws:
        auth_required = json.loads(await ws.recv())
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        auth_ok = json.loads(await ws.recv())
        if auth_ok.get("type") != "auth_ok":
            print("WebSocket authentication failed")
            return
        print(f"\nChecking for traces with errors in the last {minutes} minutes...")
        all_errors = []
        for domain in ['script', 'automation']:
            entities = await get_entities(ws, domain)
            for eid in entities:
                errors = await get_recent_traces(ws, domain, eid, minutes=minutes)
                all_errors.extend(errors)
        if not all_errors:
            print("No recent traces with errors found.")
        else:
            print(f"Found {len(all_errors)} traces with errors:")
            for err in all_errors:
                print(f"[{err['timestamp']}] {err['domain']}.{err['entity_id']} trace_id={err['trace_id'][:7]}\n  Error: {err['error']}\n")

def main():
    parser = argparse.ArgumentParser(description="Fetch recent Home Assistant automation/script trace errors via WebSocket API.")
    parser.add_argument('--ha-path', type=str, default=os.path.expanduser('~/Documents/HA-Tools/config'),
                        help='Path to Home Assistant config directory (default: ~/Documents/HA-Tools/config)')
    parser.add_argument('--minutes', type=int, default=10, help='How many minutes back to check for errors (default: 10)')
    parser.add_argument('--automations-dir', type=str, help='Path to your automations YAML folder (optional)')
    parser.add_argument('--scripts-dir', type=str, help='Path to your scripts YAML folder (optional)')
    args = parser.parse_args()
    asyncio.run(main_async(args.ha_path, minutes=args.minutes, automations_dir=args.automations_dir, scripts_dir=args.scripts_dir))

if __name__ == "__main__":
    main()
