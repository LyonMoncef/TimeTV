# History

## Features

| Feature | Files | Commit |
|---------|-------|--------|
| MCP server with TV Time tools | `server.py`, `requirements.txt`, `.mcp.json` | [`2329233`](#2026-03-01-2329233) |
| Multi-platform bot layer (Telegram, Discord, Signal) | `tvtime_client.py`, `bot_core.py`, `telegram_bot.py`, `discord_bot.py`, `signal_bot.py`, `server.py` | [`9da2a81`](#2026-03-05-9da2a81) |
| save_for_later / remove_from_for_later tools | `tvtime_client.py`, `server.py`, `bot_core.py` | [`9da2a81`](#2026-03-05-9da2a81) |

---

## Changelog

### 2026-03-05 `9da2a81`
feat: add multi-platform bot layer (Telegram, Discord, Signal) + save_for_later tool
- Extracted all TV Time API logic from server.py into tvtime_client.py (shared client singleton)
- Rewrote server.py as a thin FastMCP wrapper importing tvtime_client
- Created bot_core.py: Claude tool_use loop, SessionMemory (30min TTL, 20 msg cap), TOOL_DISPATCH, lazy Anthropic client
- Created telegram_bot.py: responds to all text messages, exits cleanly if TELEGRAM_TOKEN unset
- Created discord_bot.py: DMs and @mentions only, requires message_content intent, exits cleanly if DISCORD_TOKEN unset
- Created signal_bot.py: polls signal-cli REST API every 2s, exits cleanly if SIGNAL_NUMBER unset
- Added save_for_later(show_id): POST /user/{uid}/for_later with form-data (JSON returns 404 — discovered by testing)
- Added remove_from_for_later(show_id): DELETE /user/{uid}/for_later with form-data
- Updated requirements.txt: anthropic, python-telegram-bot, discord.py
- Updated .env.example: ANTHROPIC_API_KEY, TELEGRAM_TOKEN, DISCORD_TOKEN, SIGNAL_NUMBER, SIGNAL_API_URL
- Created FILES.md: comprehensive file index with purpose and commit references per file

### 2026-03-01 `2329233`
feat: initial MCP server for TV Time with direct API, TVMaze search, mark season watched
- Created FastMCP server with 10 tools: search_show, mark_episode_watched, mark_episode_unwatched, mark_season_watched, get_episodes_to_watch, get_watch_history, get_followed_shows, get_for_later, get_stats, get_calendar
- Replaced tvtimewrapper (HTTP Basic Auth, broken) with direct requests.Session + form-data login
- Auth via TVST_ACCESS_TOKEN header obtained from POST /v2/signin response
- search_show cross-references TVMaze (for TVDB IDs) with TV Time API (for season data)
- mark_season_watched iterates all episodes in a season and marks each individually
- Configured .mcp.json for Claude Code auto-registration (stdio transport)
