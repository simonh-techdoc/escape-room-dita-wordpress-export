# wordpress-push-online.py

import subprocess
import os
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# ===== KONFIGURATION =====
# Nur diese drei Werte anpassen:
MAP_NAME    = "main.ditamap"
MAPS_FOLDER = "maps"
WP_URL      = "https://deine-wordpress-seite.de/wp-json/wp/v2"
WP_USER     = "dein-benutzername"
WP_PASSWORD = "dein-anwendungspasswort"

# ===== AUTOMATISCHE PFADE =====
SCRIPT_DIR  = Path(__file__).parent
DITA_OT     = r"C:\DITA\dita-ot-4.4\bin\dita.bat"
MAP_FILE    = SCRIPT_DIR / MAPS_FOLDER / MAP_NAME
OUTPUT_DIR  = SCRIPT_DIR / "output-wordpress"

# ===== SCHRITT 1: DITA-OT BUILD =====
def build_dita():
    print("===== BUILD HTML-Output =====")
    print(f"Projektordner: {SCRIPT_DIR}")
    print(f"Map-Datei:     {MAP_FILE}")

    env = os.environ.copy()
    env["JAVA_HOME"] = r"C:\DITA\java25"
    env["PATH"] = r"C:\DITA\java25\bin;" + env["PATH"]

    result = subprocess.run([
        DITA_OT,
        "-i", str(MAP_FILE),
        "-f", "html5",
        "-o", str(OUTPUT_DIR),
        "--processing-mode=lax"
    ], capture_output=True, text=True, env=env)

    if result.returncode != 0:
        print("FEHLER beim Build:")
        print(result.stderr)
        return False

    print("Build erfolgreich.")
    return True

# ===== SCHRITT 2: HIERARCHIE AUS DITAMAP LESEN =====
def parse_ditamap():
    """
    Liest die Ditamap und gibt eine geordnete Liste von Dicts zurück:
    [
      { "slug": "overview", "parent_slug": None },
      { "slug": "how-it-works", "parent_slug": "overview" },
      ...
    ]
    """
    tree = ET.parse(MAP_FILE)
    root = tree.getroot()

    topics = []

    def process_topicref(topicref, parent_slug=None):
        href = topicref.get("href", "")
        if not href:
            return

        # Dateiname ohne Pfad und ohne .dita/.html-Endung
        slug = Path(href).stem

        topics.append({
            "slug":        slug,
            "parent_slug": parent_slug
        })

        # Verschachtelte topicrefs rekursiv verarbeiten
        for child in topicref.findall("topicref"):
            process_topicref(child, parent_slug=slug)

    # Alle topicrefs auf oberster Ebene verarbeiten
    for topicref in root.findall(".//topicref"):
        # Nur direkte Kinder der Map verarbeiten (nicht verschachtelte)
        pass

    # Sauberer rekursiver Durchlauf ab Map-Root
    def walk(node, parent_slug=None):
        for topicref in node.findall("topicref"):
            href = topicref.get("href", "")
            if href:
                slug = Path(href).stem
                topics.append({
                    "slug":        slug,
                    "parent_slug": parent_slug
                })
                walk(topicref, parent_slug=slug)

    walk(root)
    return topics

# ===== SCHRITT 3: HTML-DATEIEN EINLESEN =====
def read_html_files(hierarchy):
    """
    Liest HTML-Dateien ein und reichert sie mit
    Parent-Child-Info aus der Hierarchie an.
    """
    # Hierarchie als Dict für schnellen Zugriff
    hier_dict = {t["slug"]: t["parent_slug"] for t in hierarchy}

    topics = []
    for html_file in OUTPUT_DIR.rglob("*.html"):
        if html_file.name == "index.html":
            continue

        with open(html_file, encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

            title = soup.find("h1")

            article = soup.find("article")
            if not article:
                article = soup.find("main")
            if not article:
                article = soup.find("body")

            if article:
                for tag in article.find_all(True):
                    if tag.has_attr("class"):
                        del tag["class"]
                    if tag.has_attr("id"):
                        del tag["id"]

            slug = html_file.stem

            if title and article:
                topics.append({
                    "title":       title.get_text(),
                    "content":     str(article),
                    "slug":        slug,
                    "parent_slug": hier_dict.get(slug)
                })

    return topics

# ===== SCHRITT 4: IN WORDPRESS PUSHEN =====
def push_to_wordpress(topics):
    auth = (WP_USER, WP_PASSWORD)

    # Erst alle Seiten pushen und ihre WordPress-IDs merken
    # damit Parent-IDs korrekt gesetzt werden können
    slug_to_id = {}

    # Zwei Durchläufe: erst Eltern, dann Kinder
    # Sortierung: Topics ohne Parent zuerst
    sorted_topics = sorted(
        topics,
        key=lambda t: 0 if t["parent_slug"] is None else 1
    )

    for topic in sorted_topics:
        print(f"Pushe: {topic['title']}")

        # Parent-ID ermitteln
        parent_id = 0
        if topic["parent_slug"]:
            parent_id = slug_to_id.get(topic["parent_slug"], 0)
            if parent_id:
                print(f"  → Parent-ID: {parent_id}")

        # Prüfen ob Page bereits existiert
        response = requests.get(
            f"{WP_URL}/pages",
            params={"slug": topic["slug"]},
            auth=auth
        )
        existing = response.json()

        data = {
            "title":   topic["title"],
            "content": topic["content"],
            "status":  "draft",
            "slug":    topic["slug"],
            "parent":  parent_id
        }

        if existing:
            page_id = existing[0]["id"]
            r = requests.post(
                f"{WP_URL}/pages/{page_id}",
                json=data,
                auth=auth
            )
            print(f"  → Aktualisiert (ID {page_id}): {r.status_code}")
            slug_to_id[topic["slug"]] = page_id
        else:
            r = requests.post(
                f"{WP_URL}/pages",
                json=data,
                auth=auth
            )
            new_id = r.json().get("id")
            print(f"  → Neu erstellt (ID {new_id}): {r.status_code}")
            slug_to_id[topic["slug"]] = new_id

# ===== MAIN =====
if __name__ == "__main__":
    if build_dita():
        hierarchy = parse_ditamap()
        print(f"\nHierarchie aus Ditamap:")
        for t in hierarchy:
            print(f"  {t['slug']} → Parent: {t['parent_slug']}")
        topics = read_html_files(hierarchy)
        print(f"\n{len(topics)} Topics gefunden.")
        push_to_wordpress(topics)
        print("\n===== FERTIG =====")

 
 
