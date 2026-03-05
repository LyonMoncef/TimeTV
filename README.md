# TimeTV

## Problem

The official TV Time app requires manual interaction through a mobile UI. There's no way to manage your watchlist, mark episodes, or check stats via natural language or automation.

## Solution

An MCP server that wraps the TV Time API and exposes it as tools for Claude Code. Interact with TV Time in natural language — mark episodes watched, browse your lists, check stats — without opening the app.

## Features

| Tool | Description |
|------|-------------|
| `search_show` | Search for a series or movie by name |
| `mark_episode_watched` | Mark an episode as watched (supports rewatch) |
| `mark_episode_unwatched` | Mark an episode as unwatched |
| `get_episodes_to_watch` | List episodes waiting to be watched |
| `get_watch_history` | Browse watch history with pagination |
| `get_followed_shows` | List followed shows |
| `get_for_later` | List shows/movies saved for later |
| `get_stats` | Global viewing stats (hours, episodes, etc.) |
| `get_calendar` | Upcoming episodes calendar |

## Architecture

```
Claude Code
    │
    ▼ MCP protocol (stdio)
server.py (FastMCP)
    │
    ▼ HTTP (tvtimewrapper)
TV Time API
```

- **`server.py`** — FastMCP server, one tool per API endpoint
- **`tvtimewrapper`** — unofficial Python wrapper, email/password auth
- **`.mcp.json`** — registers the server with Claude Code

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your TV Time credentials
```

## Usage

Start a Claude Code session in this directory — the MCP server is loaded automatically via `.mcp.json`.

Examples:
- "Search for the show Silo"
- "What episodes do I have to watch?"
- "Mark episode 12345 as watched"
- "Show my TV Time stats"
- "What's coming up on my calendar?"

## Related projects

- [tvtimewrapper](https://pypi.org/project/tvtimewrapper/) — unofficial TV Time Python wrapper
- [FastMCP](https://github.com/jlowin/fastmcp) — Python MCP server framework
