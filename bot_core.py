import json
import os
import time

import anthropic
from dotenv import load_dotenv

import tvtime_client as tv

load_dotenv()

_client = None


def get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client

SESSION_TTL = 30 * 60  # 30 minutes
MAX_MESSAGES = 20

TOOLS = [
    {
        "name": "search_show",
        "description": "Rechercher une série ou un anime par nom. Retourne l'ID TV Time (= TVDB ID) et les saisons disponibles.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Nom de la série"},
                "limit": {"type": "integer", "description": "Nombre max de résultats"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "mark_episode_watched",
        "description": "Marquer un épisode comme vu.",
        "input_schema": {
            "type": "object",
            "properties": {
                "episode_id": {"type": "string"},
                "is_rewatch": {"type": "boolean"},
            },
            "required": ["episode_id"],
        },
    },
    {
        "name": "mark_episode_unwatched",
        "description": "Marquer un épisode comme non vu.",
        "input_schema": {
            "type": "object",
            "properties": {
                "episode_id": {"type": "string"},
            },
            "required": ["episode_id"],
        },
    },
    {
        "name": "get_episodes_to_watch",
        "description": "Obtenir la liste des épisodes à voir.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_watch_history",
        "description": "Obtenir l'historique des épisodes regardés.",
        "input_schema": {
            "type": "object",
            "properties": {
                "page": {"type": "integer"},
                "limit": {"type": "integer"},
            },
        },
    },
    {
        "name": "get_followed_shows",
        "description": "Obtenir la liste des séries suivies.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_for_later",
        "description": "Obtenir la liste des séries/films enregistrés pour plus tard.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_stats",
        "description": "Obtenir les statistiques globales de visionnage (heures, épisodes, etc.).",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "mark_season_watched",
        "description": "Marquer tous les épisodes d'une saison comme vus.",
        "input_schema": {
            "type": "object",
            "properties": {
                "show_id": {"type": "integer"},
                "season_number": {"type": "integer"},
                "is_rewatch": {"type": "boolean"},
            },
            "required": ["show_id", "season_number"],
        },
    },
    {
        "name": "get_calendar",
        "description": "Obtenir le calendrier des prochains épisodes à venir.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "save_for_later",
        "description": "Enregistrer une série ou un film dans la liste 'à regarder plus tard' sans marquer d'épisode comme vu.",
        "input_schema": {
            "type": "object",
            "properties": {
                "show_id": {"type": "integer", "description": "TVDB ID de la série ou du film"},
            },
            "required": ["show_id"],
        },
    },
    {
        "name": "remove_from_for_later",
        "description": "Retirer une série ou un film de la liste 'à regarder plus tard'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "show_id": {"type": "integer"},
            },
            "required": ["show_id"],
        },
    },
]

TOOL_DISPATCH = {
    "search_show": lambda args: tv.search_show(**args),
    "mark_episode_watched": lambda args: tv.mark_episode_watched(**args),
    "mark_episode_unwatched": lambda args: tv.mark_episode_unwatched(**args),
    "get_episodes_to_watch": lambda _: tv.get_episodes_to_watch(),
    "get_watch_history": lambda args: tv.get_watch_history(**args),
    "get_followed_shows": lambda _: tv.get_followed_shows(),
    "get_for_later": lambda _: tv.get_for_later(),
    "get_stats": lambda _: tv.get_stats(),
    "mark_season_watched": lambda args: tv.mark_season_watched(**args),
    "get_calendar": lambda _: tv.get_calendar(),
    "save_for_later": lambda args: tv.save_for_later(**args),
    "remove_from_for_later": lambda args: tv.remove_from_for_later(**args),
}

SYSTEM_PROMPT = (
    "Tu es un assistant TV Time. Tu aides l'utilisateur à gérer ses séries TV : "
    "chercher des séries, marquer des épisodes comme vus, consulter l'historique, "
    "les statistiques, le calendrier, etc. "
    "Réponds en français par défaut, sauf si l'utilisateur écrit dans une autre langue."
)


class SessionMemory:
    def __init__(self):
        self._sessions = {}

    def get_messages(self, user_id: str) -> list:
        now = time.time()
        session = self._sessions.get(user_id)
        if session is None:
            return []
        if now - session["last_active"] > SESSION_TTL:
            del self._sessions[user_id]
            return []
        return list(session["messages"])

    def add_messages(self, user_id: str, messages: list):
        now = time.time()
        if user_id not in self._sessions:
            self._sessions[user_id] = {"messages": [], "last_active": now}
        self._sessions[user_id]["messages"].extend(messages)
        self._sessions[user_id]["last_active"] = now
        msgs = self._sessions[user_id]["messages"]
        if len(msgs) > MAX_MESSAGES:
            self._sessions[user_id]["messages"] = msgs[-MAX_MESSAGES:]


_memory = SessionMemory()


def chat(user_id: str, text: str) -> str:
    history = _memory.get_messages(user_id)
    new_messages = [{"role": "user", "content": text}]
    messages = history + new_messages

    response = None
    while True:
        response = get_client().messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )
        assistant_msg = {"role": "assistant", "content": response.content}
        messages.append(assistant_msg)
        new_messages.append(assistant_msg)

        if response.stop_reason != "tool_use":
            break

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                try:
                    result = TOOL_DISPATCH[block.name](block.input)
                except Exception as e:
                    result = {"error": str(e)}
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })
        tool_msg = {"role": "user", "content": tool_results}
        messages.append(tool_msg)
        new_messages.append(tool_msg)

    _memory.add_messages(user_id, new_messages)

    if response is not None:
        for block in response.content:
            if hasattr(block, "text"):
                return block.text
    return "(pas de réponse)"
