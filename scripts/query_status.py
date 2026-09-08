import json
import sys
from datetime import datetime, timezone

import a2s

ADDRESS = ("34.59.13.79", 27015)
TIMEOUT = 5.0


def main():
    now = datetime.now(timezone.utc).isoformat()

    try:
        info = a2s.info(ADDRESS, timeout=TIMEOUT)
        try:
            players = a2s.players(ADDRESS, timeout=TIMEOUT)
            player_names = [p.name for p in players if p.name]
        except Exception:
            # A2S_PLAYER can fail (rate-limited/disabled) even when A2S_INFO
            # succeeds -- still report the server as online with just the count.
            player_names = []

        status = {
            "serverOnline": True,
            "serverName": info.server_name,
            "map": info.map_name,
            "playerCount": info.player_count,
            "maxPlayers": info.max_players,
            "currentPlayers": player_names,
            "lastUpdated": now,
        }
    except Exception as exc:
        status = {
            "serverOnline": False,
            "serverName": None,
            "map": None,
            "playerCount": 0,
            "maxPlayers": 0,
            "currentPlayers": [],
            "lastUpdated": now,
            "error": str(exc),
        }

    with open("status.json", "w") as f:
        json.dump(status, f, indent=2)

    print(json.dumps(status, indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
