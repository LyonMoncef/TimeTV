from mcp.server.fastmcp import FastMCP
import tvtime_client as tv

mcp = FastMCP("tvtime")


@mcp.tool()
def search_show(query: str, limit: int = 5) -> dict:
    """Rechercher une série ou un anime par nom. Retourne l'ID TV Time (= TVDB ID) et les saisons disponibles.
    Si aucune saison n'est trouvée pour un résultat, demander à l'utilisateur de fournir le TVDB ID manuellement."""
    return tv.search_show(query, limit)


@mcp.tool()
def mark_episode_watched(episode_id: str, is_rewatch: bool = False) -> dict:
    """Marquer un épisode comme vu"""
    return tv.mark_episode_watched(episode_id, is_rewatch)


@mcp.tool()
def mark_episode_unwatched(episode_id: str) -> dict:
    """Marquer un épisode comme non vu"""
    return tv.mark_episode_unwatched(episode_id)


@mcp.tool()
def get_episodes_to_watch() -> dict:
    """Obtenir la liste des épisodes à voir"""
    return tv.get_episodes_to_watch()


@mcp.tool()
def get_watch_history(page: int = 0, limit: int = 20) -> dict:
    """Obtenir l'historique des épisodes regardés"""
    return tv.get_watch_history(page, limit)


@mcp.tool()
def get_followed_shows() -> dict:
    """Obtenir la liste des séries suivies"""
    return tv.get_followed_shows()


@mcp.tool()
def get_for_later() -> dict:
    """Obtenir la liste des séries/films enregistrés pour plus tard"""
    return tv.get_for_later()


@mcp.tool()
def get_stats() -> dict:
    """Obtenir les statistiques globales de visionnage (heures, épisodes, etc.)"""
    return tv.get_stats()


@mcp.tool()
def mark_season_watched(show_id: int, season_number: int, is_rewatch: bool = False) -> dict:
    """Marquer tous les épisodes d'une saison comme vus"""
    return tv.mark_season_watched(show_id, season_number, is_rewatch)


@mcp.tool()
def get_calendar() -> dict:
    """Obtenir le calendrier des prochains épisodes à venir"""
    return tv.get_calendar()


@mcp.tool()
def save_for_later(show_id: int) -> dict:
    """Enregistrer une série ou un film dans la liste 'à regarder plus tard' sans marquer d'épisode comme vu"""
    return tv.save_for_later(show_id)


@mcp.tool()
def remove_from_for_later(show_id: int) -> dict:
    """Retirer une série ou un film de la liste 'à regarder plus tard'"""
    return tv.remove_from_for_later(show_id)


if __name__ == "__main__":
    mcp.run()
