# History

## Features

| Feature | Files | Commit |
|---------|-------|--------|
| MCP server with 9 TV Time tools | `server.py`, `requirements.txt`, `.mcp.json` | [`initial`](#2026-03-01-initial) |

---

## Changelog

### 2026-03-01 `initial`
feat: initial MCP server for TV Time with 9 tools
- Created FastMCP server exposing search, mark watched/unwatched, episodes to watch, watch history, followed shows, for-later list, stats, and calendar
- Configured `.mcp.json` for Claude Code auto-registration
- Documented known limitations: `show.myShows()` broken (HTTP 500), no add-to-watchlist endpoint
