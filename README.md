# TimeTV

## Problem

The official TV Time app requires manual interaction through a mobile UI. There's no way to manage your watchlist, mark episodes, or check stats via natural language or automation — and certainly not from a messaging app.

## Solution

A TV Time client exposed in two ways:
- As an **MCP server** for Claude Code — interact with TV Time in natural language inside your IDE
- As a **multi-platform bot** (Telegram, Discord, Signal) — chat with your TV Time account from any messaging app

## Features

| Tool | Description |
|------|-------------|
| `search_show` | Search for a series or movie by name (via TVMaze + TV Time) |
| `mark_episode_watched` | Mark an episode as watched (supports rewatch) |
| `mark_episode_unwatched` | Mark an episode as unwatched |
| `mark_season_watched` | Mark all episodes of a season as watched |
| `get_episodes_to_watch` | List episodes waiting to be watched |
| `get_watch_history` | Browse watch history with pagination |
| `get_followed_shows` | List followed shows |
| `get_for_later` | List shows/movies saved for later |
| `save_for_later` | Add a show or movie to the "watch later" list |
| `remove_from_for_later` | Remove a show from the "watch later" list |
| `get_stats` | Global viewing stats (hours, episodes, etc.) |
| `get_calendar` | Upcoming episodes calendar |

## Architecture

```
Claude Code / Telegram / Discord / Signal
        │
        ▼
   bot_core.py          ← Claude tool_use loop, session memory
        │
        ▼
 tvtime_client.py       ← TV Time API (api2.tozelabs.com/v2)
        │
        ▼
   TV Time API

server.py               ← thin FastMCP wrapper (MCP path only)
```

- **`tvtime_client.py`** — all TV Time API logic, singleton session, form-data auth
- **`server.py`** — FastMCP wrapper, exposes all tools via MCP protocol
- **`bot_core.py`** — Claude tool_use loop, per-user session memory (30 min TTL, 20 msg cap)
- **`telegram_bot.py`** — Telegram adapter, responds to all text messages
- **`discord_bot.py`** — Discord adapter, responds to DMs and @mentions
- **`signal_bot.py`** — Signal adapter, polls signal-cli REST API
- **`.mcp.json`** — registers the MCP server with Claude Code

## Setup

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

**.env keys:**
```
TVTIME_USERNAME=        # TV Time account
TVTIME_PASSWORD=
ANTHROPIC_API_KEY=      # required for bots
TELEGRAM_TOKEN=         # from @BotFather
DISCORD_TOKEN=          # from discord.com/developers
SIGNAL_NUMBER=          # registered Signal number
SIGNAL_API_URL=         # signal-cli-rest-api base URL (default: http://localhost:8080)
```

## Usage

**MCP (Claude Code):** start a session in this directory — the server loads automatically via `.mcp.json`.

**Telegram bot:**
```bash
.venv/bin/python telegram_bot.py
```

**Discord bot:**
```bash
.venv/bin/python discord_bot.py
```

**Signal bot** (requires [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) running):
```bash
.venv/bin/python signal_bot.py
```

Examples (natural language, any platform):
- "Quelles séries je suis ?"
- "Ajoute Loki à ma watchlist"
- "Marque l'épisode 12345 comme vu"
- "Mes stats TV Time"
- "Qu'est-ce qui sort cette semaine ?"

## Related projects

- [FastMCP](https://github.com/jlowin/fastmcp) — Python MCP server framework
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [discord.py](https://github.com/Rapptz/discord.py)
- [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api)
