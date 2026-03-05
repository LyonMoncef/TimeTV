# Notes

## Known Issues

- **`show.myShows()` returns HTTP 500** — this tvtimewrapper method is broken on the API side. Not exposed as an MCP tool. Use `get_followed_shows` instead.
- **No "add to watchlist" method** — `tvtimewrapper` does not expose an endpoint to add a show to the watchlist or "for later" list. Adding shows must be done through the official app.
- **Token expiry** — TV Time auth tokens expire roughly every 5 days. The client singleton (`_client`) will need to be reset if auth errors occur. A restart of the MCP server is sufficient.

## Backlog

- Auto re-auth on token expiry (catch auth error, reset `_client`, retry)
- `get_show_details` tool — fetch episodes list and metadata for a specific show
- `get_user_profile` tool — expose `user.profile()` as an MCP tool
- Signal adapter: needs bbernhard/signal-cli-rest-api docker image running; number must be registered
- bot_core session memory is in-process only — restarting the bot resets all conversations
- bot_core.chat() is synchronous; fine for personal use but will block the event loop under load
- WhatsApp adapter (not yet implemented) — would need a WhatsApp Business API gateway
