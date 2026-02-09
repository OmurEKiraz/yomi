import re
from urllib.parse import unquote

def parse_chapter_metadata(chapter_title: str, series_title: str, url: str) -> dict:
    """
    Extracts chapter number and subtitle from both the Chapter Title and URL.
    This dual-check ensures higher accuracy for oddly named chapters.
    """
    meta_number = ""
    meta_subtitle = ""
    
    # 1. Cleanup: Prepare inputs for analysis
    clean_title = chapter_title.strip()
    clean_url = unquote(url).strip().lower()
    
    # --- METHOD A: Try from Title ---
    # Regex catches: Chapter X, Ch. X, No. X, Episode X
    match_title = re.search(r'(?:chapter|ch\\.?|no\\.?|episode)\s*(\d+(\.\d+)?)', clean_title, re.IGNORECASE)
    
    if match_title:
        meta_number = match_title.group(1)
        # Isolate subtitle (e.g., "Chapter 5: The End" -> "The End")
        meta_subtitle = re.sub(r'(?:chapter|ch\\.?|no\\.?|episode)\s*(\d+(\.\d+)?)[\\s:-]*', '', clean_title, flags=re.IGNORECASE).strip()
    
    # --- METHOD B: Fallback to URL ---
    if not meta_number:
        # Look for patterns like /chapter-123/ or /c123/ in URL
        match_url = re.search(r'/(?:chapter|ch|c)[-/_]?(\d+(\.\d+)?)(?:/|$)', clean_url)
        if match_url:
            meta_number = match_url.group(1)
        else:
             meta_number = "0" # Default if nothing found

    if not meta_subtitle:
        meta_subtitle = clean_title

    return {
        "series": series_title,
        "number": meta_number,
        "title": meta_subtitle,
        "web": url,
        "original_title": chapter_title
    }

def generate_comic_info_xml(metadata: dict) -> str:
    """
    Generates a ComicInfo.xml string compliant with standard comic readers.
    """
    def clean(val):
        return str(val).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    series = clean(metadata.get('series', ''))
    title = clean(metadata.get('title', ''))
    number = clean(metadata.get('number', ''))
    web = clean(metadata.get('web', ''))
    
    writer = clean(metadata.get('writer', ''))
    artist = clean(metadata.get('artist', ''))
    genres = clean(metadata.get('genres', ''))
    summary = clean(metadata.get('summary', ''))
    year = clean(metadata.get('year', ''))

    return f"""<?xml version="1.0"?>
<ComicInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Series>{series}</Series>
  <Number>{number}</Number>
  <Title>{title}</Title>
  <Web>{web}</Web>
  <Writer>{writer}</Writer>
  <Penciller>{artist}</Penciller>
  <Genre>{genres}</Genre>
  <Summary>{summary}</Summary>
  <Year>{year}</Year>
</ComicInfo>"""