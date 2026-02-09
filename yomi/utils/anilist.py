import aiohttp
import logging
from difflib import SequenceMatcher

logger = logging.getLogger("YomiCore")

class AniListProvider:
    """
    Provides metadata fetching capabilities using the AniList GraphQL API.
    """
    def __init__(self):
        self.api_url = 'https://graphql.anilist.co'
        self.cache = {}

    def calculate_similarity(self, a, b):
        """Calculates string similarity ratio between 0 and 1."""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    async def fetch_metadata(self, manga_name: str):
        """
        Fetches metadata for a given manga name.
        Uses fuzzy matching to ensure the result matches the query.
        """
        if manga_name in self.cache:
            return self.cache[manga_name]

        query = '''
        query ($search: String) {
          Media (search: $search, type: MANGA) {
            title { romaji english }
            staff {
              edges {
                role
                node { name { full } }
              }
            }
            startDate { year }
            genres
            description
          }
        }
        '''
        variables = {'search': manga_name}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json={'query': query, 'variables': variables}, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        media = data.get('data', {}).get('Media')
                        
                        if not media: return None
                        
                        # Fuzzy match verification to avoid incorrect metadata
                        titles = [media['title']['romaji'], media['title']['english']]
                        best_match = max([self.calculate_similarity(manga_name, t) for t in titles if t])
                        
                        # Threshold set to 0.7 to accept slight variations
                        if best_match > 0.6:
                            meta = self._format_meta(media)
                            self.cache[manga_name] = meta
                            return meta
        except Exception as e:
            logger.debug(f"AniList API Error: {e}")
        return None

    def _format_meta(self, media):
        writer, artist = "", ""
        if 'staff' in media and 'edges' in media['staff']:
            for edge in media['staff']['edges']:
                role, name = edge['role'].lower(), edge['node']['name']['full']
                if 'story' in role or 'writer' in role: writer = name
                if 'art' in role or 'illustrator' in role: artist = name
        
        desc = media.get('description', '')
        if desc:
            desc = desc.replace("<br>", "\n").strip()

        return {
            "writer": writer or artist,
            "artist": artist or writer,
            "year": media.get('startDate', {}).get('year', ''),
            "genres": ", ".join(media.get('genres', [])),
            "summary": desc
        }