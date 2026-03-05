import os
import requests
from dotenv import load_dotenv

load_dotenv()

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


def search_show(query: str, limit: int = 5) -> dict:
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


def mark_episode_watched(episode_id: str, is_rewatch: bool = False) -> dict:
    s, _ = get_session()
    return s.post(f"{BASE_URL}/watched_episodes/episode/{episode_id}", params={"is_rewatch": 1 if is_rewatch else 0}).json()


def mark_episode_unwatched(episode_id: str) -> dict:
    s, _ = get_session()
    return s.delete(f"{BASE_URL}/watched_episodes/episode/{episode_id}").json()


def get_episodes_to_watch() -> dict:
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/to_watch").json()


def get_watch_history(page: int = 0, limit: int = 20) -> dict:
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/watched_episodes", params={"page": page, "limit": limit, "include_recent_watchers": 1}).json()


def get_followed_shows() -> dict:
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/followed_shows").json()


def get_for_later() -> dict:
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/for_later").json()


def get_stats() -> dict:
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/stats").json()


def mark_season_watched(show_id: int, season_number: int, is_rewatch: bool = False) -> dict:
    s, _ = get_session()
    episodes = s.get(f"{BASE_URL}/show/{show_id}/seasons/{season_number}").json()
    results = []
    for ep in episodes:
        r = s.post(f"{BASE_URL}/watched_episodes/episode/{ep['id']}", params={"is_rewatch": 1 if is_rewatch else 0}).json()
        results.append({"episode": ep["number"], "name": ep["name"], "result": r.get("result")})
    return {"season": season_number, "marked": len(results), "episodes": results}


def get_calendar() -> dict:
    s, uid = get_session()
    return s.get(f"{BASE_URL}/user/{uid}/calendar").json()


def save_for_later(show_id: int) -> dict:
    s, uid = get_session()
    return s.post(f"{BASE_URL}/user/{uid}/for_later", data={"show_id": show_id}).json()


def remove_from_for_later(show_id: int) -> dict:
    s, uid = get_session()
    return s.delete(f"{BASE_URL}/user/{uid}/for_later", data={"show_id": show_id}).json()
