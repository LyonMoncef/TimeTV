# Files

Comprehensive index of every source file in the TimeTV project, its purpose, and the commits that touched it.

---

## Root Configuration

| File | Purpose | Commits |
|------|---------|---------|
| `.gitignore` | Git ignore rules — `.env`, `.venv`, `__pycache__`, `.mcp.json` secrets | `2329233` |
| `.env.example` | Template for all environment variables (TV Time, Anthropic, Telegram, Discord, Signal) | `2329233`, `9da2a81` |
| `.mcp.json` | Claude Code MCP auto-registration — stdio transport, `python server.py` | `2329233` |
| `requirements.txt` | Python dependencies — mcp, python-dotenv, requests, anthropic, python-telegram-bot, discord.py | `2329233`, `9da2a81` |

## Project Documentation

| File | Purpose | Commits |
|------|---------|---------|
| `README.md` | Project overview — problem, solution, features table, architecture diagram, setup, usage examples | `2329233`, `9da2a81` |
| `NOTES.md` | Known issues and backlog items | `2329233`, `9da2a81` |
| `HISTORY.md` | Features table + detailed commit-by-commit changelog | `2329233`, `9da2a81` |
| `FILES.md` | This file — comprehensive file index with purposes and commit references | `9da2a81` |

---

## Core

### TV Time API Client

| File | Purpose | Commits |
|------|---------|---------|
| `tvtime_client.py` | All TV Time API logic — singleton `requests.Session`, form-data login, `TVST_ACCESS_TOKEN` auth, all query/mutation functions | `9da2a81` |

**Functions exposed by `tvtime_client.py`:**

| Function | Endpoint | Notes |
|----------|----------|-------|
| `get_session()` | `POST /v2/signin` | Singleton — initialises once, reuses session |
| `search_show(query, limit)` | TVMaze + `GET /v2/show/{id}` + `/seasons` | Cross-references TVMaze TVDB IDs with TV Time |
| `mark_episode_watched(episode_id, is_rewatch)` | `POST /v2/watched_episodes/episode/{id}` | |
| `mark_episode_unwatched(episode_id)` | `DELETE /v2/watched_episodes/episode/{id}` | |
| `mark_season_watched(show_id, season_number, is_rewatch)` | `GET /v2/show/{id}/seasons/{n}` + batch POST | Iterates all episodes in season |
| `get_episodes_to_watch()` | `GET /v2/user/{uid}/to_watch` | |
| `get_watch_history(page, limit)` | `GET /v2/user/{uid}/watched_episodes` | |
| `get_followed_shows()` | `GET /v2/user/{uid}/followed_shows` | |
| `get_for_later()` | `GET /v2/user/{uid}/for_later` | |
| `save_for_later(show_id)` | `POST /v2/user/{uid}/for_later` (form-data) | Discovered by testing — JSON returns 404, form returns 200 |
| `remove_from_for_later(show_id)` | `DELETE /v2/user/{uid}/for_later` (form-data) | Same pattern — show_id must be in body, not URL |
| `get_stats()` | `GET /v2/user/{uid}/stats` | |
| `get_calendar()` | `GET /v2/user/{uid}/calendar` | |

---

### MCP Server

| File | Purpose | Commits |
|------|---------|---------|
| `server.py` | FastMCP wrapper — one `@mcp.tool()` per `tvtime_client` function, no logic of its own | `2329233`, `9da2a81` |

**Evolution:** originally contained all API logic inline; refactored in `9da2a81` to delegate to `tvtime_client.py`.

---

### Bot Core

| File | Purpose | Commits |
|------|---------|---------|
| `bot_core.py` | Shared bot logic — Claude tool_use loop, `SessionMemory`, `chat(user_id, text) -> str` | `9da2a81` |

**Key components:**

| Component | Description |
|-----------|-------------|
| `TOOLS` | Anthropic tool definitions for all 12 TV Time functions |
| `TOOL_DISPATCH` | `dict[name -> lambda(args)]` mapping tool calls to `tvtime_client` functions |
| `SYSTEM_PROMPT` | French-default assistant persona |
| `SessionMemory` | In-memory per-user message history — 30 min TTL, 20 message cap |
| `get_client()` | Lazy Anthropic client init (defers `ANTHROPIC_API_KEY` check to first chat call) |
| `chat(user_id, text)` | Synchronous Claude tool_use loop — runs until `stop_reason != "tool_use"` |

---

## Bot Adapters

| File | Purpose | Commits |
|------|---------|---------|
| `telegram_bot.py` | Telegram adapter — responds to all text messages; exits cleanly if `TELEGRAM_TOKEN` unset | `9da2a81` |
| `discord_bot.py` | Discord adapter — responds to DMs and @mentions only; requires `message_content` intent; exits cleanly if `DISCORD_TOKEN` unset | `9da2a81` |
| `signal_bot.py` | Signal adapter — polls signal-cli REST API every 2s; exits cleanly if `SIGNAL_NUMBER` unset | `9da2a81` |
