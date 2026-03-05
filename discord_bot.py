import os
import sys

import discord
from dotenv import load_dotenv

import bot_core

load_dotenv()

TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    print("DISCORD_TOKEN not set", file=sys.stderr)
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Discord bot ready as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mention = client.user in message.mentions
    if not is_dm and not is_mention:
        return
    text = message.content.replace(f"<@{client.user.id}>", "").strip()
    if not text:
        return
    user_id = str(message.author.id)
    reply = bot_core.chat(user_id, text)
    await message.channel.send(reply)


if __name__ == "__main__":
    client.run(TOKEN)
