from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import os

load_dotenv()

mcp = FastMCP("tvtime")

BASE_URL = "https://api2.tozelabs.com/v2"

_session = None
_user_id = None


def get_session():
    global _session, _user_id
    if _session is None:
        s = requests.Session()
        r = s.post(f"{BASE_URL}/signin", data={
            "username": os.environ["TVTIME_USERNAME"],
            "password": os.environ["TVTIME_PASSWORD"],
        }).json()
        if r.get("result") == "KO":
            raise RuntimeError(r.get("message", "Login failed"))
        _user_id = r["id"]
        s.headers.update({"TVST_ACCESS_TOKEN": r["tvst_access_token"]})
        _session = s
    return _session, _user_id


@mcp.tool()
def search_show(query: str, limit: int = 5) -> dict:
    """Rechercher une série ou un anime par nom. Retourne l'ID TV Time (= TVDB ID) et les saisons disponibles.
    Si aucune saison n'est trouvée pour un résultat, demander à l'utilisateur de fournir le TVDB ID manuellement."""
    s, _ = get_session()
    tvmaze_results = requests.get("https://api.tvmaze.com/search/shows", params={"q": query}).json()

    results = []
    for item in tvmaze_results[:limit]:
        show = item["show"]
        tvdb_id = show.get("externals", {}).get("thetvdb")
        if not tvdb_id:
            continue
        tv = s.get(f"{BASE_URL}/show/{tvdb_id}").json()
        if "error" in tv:
            continue
        seasons = s.get(f"{BASE_URL}/show/{tvdb_id}/seasons").json().get("seasons", [])
        entry = {
            "id": tvdb_id,
            "name": tv.get("name"),
            "status": tv.get("status"),
            "network": tv.get("network"),
            "seasons": seasons,
        }
        if not seasons:
            entry["warning"] = "Aucune donnée d'épisodes sur TV Time. Chercher le bon TVDB ID sur thetvdb.com ou tvmaze.com."
        results.append(entry)
    return {"results": results}


@mcp.tool()
def mark_episode_watched(episode_id: str, is_rewatch: bool = False) -> dict:
    """Marquer un épisode comme vu"""
    s, _ = get_session()
    return s.post(f"{BASE_URL}/watched_episodes/episode/{episode_id}", params={"is_rewatch": 1 if is_rewatch else 0}).json()


@mcp.tool()
def mark_episode_unwatched(episode_id: str) -> dict:
    """Marquer un épisode comme non vu"""
    s, _ = get_session()
    return s.delete(f"{BASE_URL}/watched_episodes/episode/{episode_id}").json()


@mcp.tool()
def get_episodes_to_watch() -> dict:
    """Obtenir la liste des épisodes à voir"""
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/to_watch").json()


@mcp.tool()
def get_watch_history(page: int = 0, limit: int = 20) -> dict:
    """Obtenir l'historique des épisodes regardés"""
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/watched_episodes", params={"page": page, "limit": limit, "include_recent_watchers": 1}).json()


@mcp.tool()
def get_followed_shows() -> dict:
    """Obtenir la liste des séries suivies"""
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/followed_shows").json()


@mcp.tool()
def get_for_later() -> dict:
    """Obtenir la liste des séries/films enregistrés pour plus tard"""
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/for_later").json()


@mcp.tool()
def get_stats() -> dict:
    """Obtenir les statistiques globales de visionnage (heures, épisodes, etc.)"""
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/stats").json()


@mcp.tool()
def mark_season_watched(show_id: int, season_number: int, is_rewatch: bool = False) -> dict:
    """Marquer tous les épisodes d'une saison comme vus"""
    s, _ = get_session()
    episodes = s.get(f"{BASE_URL}/show/{show_id}/seasons/{season_number}").json()
    results = []
    for ep in episodes:
        r = s.post(f"{BASE_URL}/watched_episodes/episode/{ep['id']}", params={"is_rewatch": 1 if is_rewatch else 0}).json()
        results.append({"episode": ep["number"], "name": ep["name"], "result": r.get("result")})
    return {"season": season_number, "marked": len(results), "episodes": results}


@mcp.tool()
def get_calendar() -> dict:
    """Obtenir le calendrier des prochains épisodes à venir"""
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/calendar").json()


if __name__ == "__main__":
    mcp.run()
