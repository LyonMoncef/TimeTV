# History

## Features

| Feature | Files | Commit |
|---------|-------|--------|
| MCP server with 9 TV Time tools | `server.py`, `requirements.txt`, `.mcp.json` | [`initial`](#2026-03-01-initial) |
| Multi-platform bot layer (Telegram, Discord, Signal) | `tvtime_client.py`, `bot_core.py`, `telegram_bot.py`, `discord_bot.py`, `signal_bot.py`, `server.py` | [`bot-layer`](#2026-03-05-bot-layer) |

---

## Changelog

### 2026-03-05 `bot-layer`
feat: add multi-platform bot layer with Telegram, Discord, and Signal adapters
- Extracted all TV Time API logic from server.py into tvtime_client.py (shared client)
- Rewrote server.py as a thin MCP wrapper importing tvtime_client
- Created bot_core.py: Claude tool_use loop, per-user session memory (30min TTL, 20 msg cap), TOOL_DISPATCH
- Created telegram_bot.py: responds to all text messages, exits cleanly if TELEGRAM_TOKEN unset
- Created discord_bot.py: responds to DMs and @mentions only, exits cleanly if DISCORD_TOKEN unset
- Created signal_bot.py: polls signal-cli REST API, exits cleanly if SIGNAL_NUMBER unset
- Updated requirements.txt with anthropic, python-telegram-bot, discord.py
- Updated .env.example with ANTHROPIC_API_KEY, TELEGRAM_TOKEN, DISCORD_TOKEN, SIGNAL_NUMBER, SIGNAL_API_URL

### 2026-03-01 `initial`
feat: initial MCP server for TV Time with 9 tools
- Created FastMCP server exposing search, mark watched/unwatched, episodes to watch, watch history, followed shows, for-later list, stats, and calendar
- Configured `.mcp.json` for Claude Code auto-registration
- Documented known limitations: `show.myShows()` broken (HTTP 500), no add-to-watchlist endpoint
