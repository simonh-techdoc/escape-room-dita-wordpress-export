# wordpress-push-offline.py

import subprocess
import os
from pathlib import Path
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# ===== KONFIGURATION =====
# Nur diese zwei Werte anpassen:
MAP_NAME    = "main.ditamap"
MAPS_FOLDER = "maps"

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
    tree = ET.parse(MAP_FILE)
    root = tree.getroot()

    topics = []

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

# ===== SCHRITT 3: HTML-DATEIEN BEREINIGEN =====
def clean_html_files():
    print("===== BEREINIGE HTML-Dateien =====")

    for html_file in OUTPUT_DIR.rglob("*.html"):
        with open(html_file, encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        for tag in soup.find_all(True):
            if tag.has_attr("class"):
                del tag["class"]
            if tag.has_attr("id"):
                del tag["id"]

        for link in soup.find_all("link", rel="stylesheet"):
            link["href"] = str(OUTPUT_DIR / "commonltr.css")

        html_file.write_text(str(soup), encoding="utf-8")
        print(f"  → Bereinigt: {html_file.name}")

# ===== SCHRITT 4: LOKALE LINKS FIXEN =====
def fix_local_links():
    print("===== FIXE LOKALE LINKS =====")

    index = OUTPUT_DIR / "index.html"
    if index.exists():
        content = index.read_text(encoding="utf-8")
        content = content.replace("../topics/", "topics/")
        index.write_text(content, encoding="utf-8")
        print("  → index.html gefixt")

# ===== SCHRITT 5: HIERARCHIE-REPORT AUSGEBEN =====
def list_topics(hierarchy):
    print("\n===== HIERARCHIE AUS DITAMAP =====")
    for t in hierarchy:
        if t["parent_slug"]:
            print(f"  {t['parent_slug']} → {t['slug']}")
        else:
            print(f"  [Root] {t['slug']}")

    print("\n===== ERZEUGTE DATEIEN =====")
    for html_file in sorted(OUTPUT_DIR.rglob("*.html")):
        print(f"  {html_file}")

# ===== MAIN =====
if __name__ == "__main__":
    if build_dita():
        hierarchy = parse_ditamap()
        clean_html_files()
        fix_local_links()
        list_topics(hierarchy)
        print("\n===== FERTIG =====")

 
