"""
automation_watchdog.py

Watches Home Assistant automations in real time and reports failures using the WebSocket API.

- Connects to your Home Assistant instance via WebSocket.
- Subscribes to automation trigger events and fetches traces for each run.
- Reports errors and exceptions with timing information.
- Supports filtering by automation entity_id (include/exclude).

Usage:
  python automation_watchdog.py --ha-path <HA_CONFIG_PATH> [--timeout SECONDS] [--include a,b] [--exclude x,y]

Arguments:
  --ha-path <HA_CONFIG_PATH>   Path to the Home Assistant config directory (required)
  --timeout SECONDS           Seconds to wait before fetching trace (default: 3)
  --include a,b               Comma-separated list of automations to watch
  --exclude x,y               Comma-separated list of automations to ignore

Requires: websockets==12.0
"""
import argparse, asyncio, json, sys, datetime, os
import websockets

BAD_STATES = {"error", "exception"}

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_WHITE = "\033[97m"

# Utility print functions
def print_error(msg):
    print(f"{COLOR_RED}{msg}{COLOR_RESET}", file=sys.stderr)

def print_success(msg):
    print(f"{COLOR_GREEN}{msg}{COLOR_RESET}")

def print_warning(msg):
    print(f"{COLOR_YELLOW}{msg}{COLOR_RESET}")

def print_info(msg):
    print(f"{COLOR_BLUE}{msg}{COLOR_RESET}")

def log(msg: str):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {msg}", flush=True)

def load_ha_config(ha_path):
    config_path = os.path.join(ha_path, 'ha_config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

async def monitor(url: str, token: str, timeout: float,
                  include: set[str] | None, exclude: set[str] | None):
    async with websockets.connect(url) as ws:
        await ws.recv()                                    # auth_required
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        auth_ok = json.loads(await ws.recv())
        if auth_ok.get("type") != "auth_ok":
            sys.exit("✖  WebSocket authentication failed")

        await ws.send(json.dumps({
            "id": 1, "type": "subscribe_events",
            "event_type": "automation_triggered"
        }))

        pending: dict[str, tuple[str, float]] = {}
        trace_futures: dict[str, asyncio.Future] = {}
        log("★ Watchdog running…  (Ctrl-C to quit)")

        async def trace_request(ctx, ent):
            await asyncio.sleep(timeout)
            max_retries = 3
            reply = None
            for attempt in range(max_retries):
                req_id = f"trace_{ctx}_{attempt}"
                fut = asyncio.get_event_loop().create_future()
                trace_futures[req_id] = fut
                await ws.send(json.dumps({
                    "id": req_id,
                    "type": "trace/get",
                    "domain": "automation",
                    "item_id": ent.split(".", 1)[1],
                    "run_id": ctx
                }))
                try:
                    reply = await asyncio.wait_for(fut, timeout=2)
                except asyncio.TimeoutError:
                    reply = None
                finally:
                    trace_futures.pop(req_id, None)
                if reply and reply.get("success"):
                    break
                if attempt < max_retries - 1:
                    await asyncio.sleep(0.5)
            pending.pop(ctx, None)
            if not reply or not reply.get("success"):
                print_error(f"⚠  Couldn’t fetch trace for {ent} (run {ctx[:7]}) after {max_retries} attempts")
                return
            trace = reply["result"]["trace"]
            outcome = trace[-1]["result"]
            took_ms = trace[-1]["timestamp"] - trace[0]["timestamp"]
            if outcome in BAD_STATES:
                log(f"❌  {ent} failed after {took_ms:.0f} ms  (run {ctx[:7]})")

        while True:
            msg = json.loads(await ws.recv())
            # Route trace responses to the correct future
            if "id" in msg and str(msg["id"]).startswith("trace_"):
                fut = trace_futures.get(str(msg["id"]))
                if fut and not fut.done():
                    fut.set_result(msg)
                continue
            if msg.get("type") == "event":
                data = msg["event"]["data"]
                ent  = data["entity_id"]
                if include and ent not in include:
                    continue
                if exclude and ent in exclude:
                    continue
                ctx  = msg["event"]["context"]["id"]
                pending[ctx] = (ent, asyncio.get_event_loop().time())
                asyncio.create_task(trace_request(ctx, ent))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ha-path", type=str, default=os.environ.get('HA_CONFIG_PATH'),
                   help="Path to Home Assistant config directory (required)")
    p.add_argument("--timeout", type=float, default=3,
                   help="Seconds to wait before fetching trace")
    p.add_argument("--include", help="Comma-separated list of automations to watch")
    p.add_argument("--exclude", help="Comma-separated list of automations to ignore")
    args = p.parse_args()

    if not args.ha_path:
        print_error('You must specify --ha-path or set the HA_CONFIG_PATH environment variable.')
        exit(1)

    ha_config = load_ha_config(args.ha_path)
    url = ha_config['HA_URL'].replace('https://', 'wss://').replace('http://', 'ws://')
    if not url.endswith('/api/websocket'):
        url = url.rstrip('/') + '/api/websocket'
    token = ha_config['HA_TOKEN']

    include = set(args.include.split(",")) if args.include else None
    exclude = set(args.exclude.split(",")) if args.exclude else None
    try:
        asyncio.run(monitor(url, token, args.timeout, include, exclude))
    except KeyboardInterrupt:
        print("\nBye!")
