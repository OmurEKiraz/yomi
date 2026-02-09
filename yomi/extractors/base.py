import abc
import os
import requests
from urllib.parse import urlparse
from curl_cffi import requests as curl_requests  # Used for Cloudflare bypassing

class BaseExtractor(abc.ABC):
    """
    Abstract Base Class for Manga Extractors.
    
    Implements a hybrid approach:
    - curl_cffi: For scraping and bypassing anti-bot protections (Cloudflare).
    - requests: For reliable binary file downloading (images).
    """

    def __init__(self, proxy: str = None):
        # 1. Scraper Session (Impersonates Chrome to bypass WAF)
        self.scraper = curl_requests.Session(impersonate="chrome120")
        self.scraper.headers.update({
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

        # 2. Downloader Session (Standard Request Handling)
        self.downloader = requests.Session()
        self.downloader.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://google.com"
        })

        if proxy:
            self.scraper.proxies = {"http": proxy, "https": proxy}
            self.downloader.proxies = {"http": proxy, "https": proxy}

    def _sanitize_url(self, url: str) -> str:
        """Cleans and validates the URL."""
        return url.strip()

    def download_image(self, url: str, save_path: str, source_chapter_url: str = None) -> bool:
        """
        Downloads an image with a multi-strategy retry mechanism.
        Attempts different Referer headers to bypass hotlink protection.
        """
        clean_url = self._sanitize_url(url)
        parsed_uri = urlparse(clean_url)
        root_domain = f"{parsed_uri.scheme}://{parsed_uri.netloc}/"

        # Retry Strategies for Hotlink Protection
        strategies = [
            {"Referer": source_chapter_url if source_chapter_url else ""},  # Strategy 1: Chapter Referer
            {"Referer": ""},                                                # Strategy 2: No Referer
            {"Referer": root_domain}                                        # Strategy 3: Root Domain
        ]

        for headers in strategies:
            try:
                self.downloader.headers.update(headers)
                
                # Stream the download to handle large files efficiently
                response = self.downloader.get(clean_url, stream=True, timeout=20)
                
                if response.status_code == 200:
                    # Filter out ghost files (0 bytes)
                    if len(response.content) == 0:
                        continue 
                        
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    
                    # Verify file integrity on disk
                    if os.path.getsize(save_path) > 0:
                        return True
                    
            except Exception:
                continue # Fail silently and try next strategy

        return False