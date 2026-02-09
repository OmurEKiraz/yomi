# YOMI - The Universal Hybrid-Engine Manga Downloader

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Status](https://img.shields.io/badge/Status-Beta_v0.1.0-orange?style=flat)

**Yomi** is a command-line utility designed for the long-term archival of manga. It features a hybrid scraping engine that combines high-speed asynchronous requests with browser simulation to bypass modern bot protections (Cloudflare, DDOS-Guard).

Unlike standard downloaders, Yomi focuses on **metadata integrity** and **mirror persistence**. It automatically fetches metadata (Author, Artist, Summary) from AniList and embeds it into `.cbz` files, making them ready for media servers and Comic Book Reader apps.

## ✨ Key Features

* **Dynamic Mirror Resolution:** Automatically detects when a site changes domains (e.g., `site-w1.com` -> `site-w2.com`) and updates the target on the fly using a remote database.
* **Smart Metadata:** Fetches official metadata from AniList and embeds it directly into `ComicInfo.xml`.
* **Hybrid Engine:** Uses `aiohttp` for speed and `curl_cffi` for bypassing anti-bot protections.
* **Format Agnostic:** Export as raw directories, **PDF** documents, or **CBZ** archives.
* **Remote Database:** Fetches the latest site definitions from GitHub on every run. No need to update the package manually for new mangas.

---

## 🛠️ Installation

### Option 1: Install via PyPI (Recommended)
The easiest way to install Yomi is through pip.

###### pip install yomi-core


### Option 2: Build from Source (For Developers)
If you want to contribute or use the latest unreleased features:


###### git clone [https://github.com/OmurEKiraz/yomi-core.git](https://github.com/OmurEKiraz/yomi-core.git)
###### cd yomi-core
###### pip install .




## 📖 Usage
Yomi is controlled entirely via the Command Line Interface (CLI)
##### 1. Basic CommandsTo see all available commands and options, use the help flag: 

###### yomi --help


##### 2. Downloading Manga
You can download by providing a direct URL or a known slug.
###### Basic Download (Default: Folder format): yomi download -u "[https://read-site.com/manga/bleach](https://read-site.com/manga/bleach)"
###### Archival Format (.CBZ with Metadata):Best for cbz reader apps. yomi download -u "bleach" -f cbz
###### Portable Format (.PDF):Best for tablets/phones.Bashyomi download -u "berserk" -f pdf

##### 3. Advanced Options 

###### -r / --rangeDownload specific chapters.-r "10-20" or -r "1050"

###### -w / --workersSet concurrent download threads.-w 16 (Default: 8)

###### -o / --outSet custom output directory.-o "D:/MangaArchive"

###### -p / --proxyUse a proxy server.-p "http://127.0.0.1:8080"

###### --debugEnable verbose logging for debugging.--debug

## 4. Search & Library
Check which sites are currently supported or search for a specific series in the database.

#### Search for a series

##### yomi available -s "vinland saga"

####  List all supported sites

##### yomi available --all

# ⚙️ Configuration
Yomi fetches its site configurations dynamically from the remote repository. You do not need to update the package manually to get support for new sites. The engine automatically checks for the latest definitions on every run.

# ⚖️ Disclaimer
Yomi is a tool developed for educational purposes and personal archiving for already open to public contents. The developers do not endorse or support copyright infringement. Please support the creators by purchasing official releases.

License: MIT