# DITA-to-WordPress Publishing Workflow

## Überblick

Automatisierter Publishing-Workflow der DITA-Quelldateien in einem
einzigen Schritt zu HTML, PDF und WordPress-Pages verarbeitet.
Entwickelt als Nebenprojekt zur IHK-Weiterbildung Technische Redaktion.

---

## Projektstruktur

```
projektordner/
├── maps/
│   ├── main.ditamap          # Hauptmap mit Hierarchie
│   └── keys.ditamap          # Key-Definitionen (Variablen)
├── topics/
│   ├── overview.dita         # Concept-Topic
│   ├── how-it-works.dita     # Task-Topic
│   └── cta.dita              # Task-Topic
├── output-html/              # HTML5-Output (automatisch generiert)
├── output-pdf/               # PDF-Output (automatisch generiert)
├── output-wordpress/         # WordPress-Output (automatisch generiert)
├── DITA-build-HTML+PDF.bat   # Build-Skript für HTML und PDF
├── wordpress-push-online.py  # Publishing-Skript für WordPress (online)
└── wordpress-push-offline.py # Publishing-Skript für lokale Ausgabe
```

---

## Technischer Stack

| Komponente | Technologie |
|---|---|
| Authoring-Format | DITA 1.3 (XML) |
| Build-Engine | DITA-OT 4.4 |
| Laufzeitumgebung | Java 17 (portabel) |
| Ausgabeformate | HTML5, PDF, WordPress |
| Automatisierung | Windows Batch, Python 3 |
| WordPress-Anbindung | REST API v2 |
| HTML-Verarbeitung | BeautifulSoup4 |

---

## Workflow

### 1. Authoring in DITA

Inhalte werden in oXygen XML Editor oder Notepad++ als DITA-Topics
erstellt – strikt nach Topic-Typen getrennt:

- **Concept** – beschreibt Was (`<conbody>`)
- **Task** – beschreibt Wie (`<steps>`, `<cmd>`)
- **Reference** – tabellarische Referenzinformationen

Variablen wie Produktnamen oder Zeitangaben werden als Keys in einer
separaten `keys.ditamap` verwaltet und per `<ph keyref="..."/>` 
eingebunden. Eine Änderung am Key aktualisiert automatisch alle
Verwendungsstellen in allen Ausgabeformaten.

### 2. Build: HTML und PDF

```batch
DITA-build-HTML+PDF.bat
```

Das Batch-Skript führt folgende Schritte aus:

1. Portables Java 17 aktivieren
2. Output-Ordner bereinigen
3. DITA-OT-Build HTML5
4. DITA-OT-Build PDF
5. Link-Korrektur per PowerShell
6. Outputs automatisch öffnen

Beide Outputs entstehen aus derselben DITA-Quelle – kein doppeltes
Pflegen, keine Synchronisationsfehler.

### 3. Publishing: WordPress

**Online (echter WordPress-Server):**

```bash
python wordpress-push-online.py
```

1. DITA-OT-Build HTML5
2. Ditamap parsen → Parent-Child-Hierarchie ermitteln
3. HTML-Dateien einlesen, DITA-CSS-Klassen entfernen
4. Per WordPress REST API pushen:
   - Slug-Abgleich: bestehende Seiten werden aktualisiert,
     neue Seiten werden erstellt (keine Duplikate)
   - Parent-Child-Beziehung aus Ditamap wird als
     WordPress-Seitenhierarchie abgebildet
   - Status: `draft` (manuelle Freigabe in WordPress)

**Offline (lokale Ausgabe):**

```bash
python wordpress-push-offline.py
```

Gleicher Build-Prozess, aber ohne WordPress-Anbindung.
CSS-Pfade werden auf absolute lokale Pfade korrigiert,
Links werden gefixt. Hierarchie-Report wird ausgegeben.

---

## Konfiguration

### Batch-Skript

Keine Anpassung nötig solange die Projektstruktur gleich bleibt.
`MAP_FILE` wird automatisch aus dem Skript-Speicherort abgeleitet.

### Python-Skripte

Nur diese Werte anpassen:

```python
MAP_NAME    = "main.ditamap"    # Name der Ditamap
MAPS_FOLDER = "maps"            # Unterordner der Ditamap
```

Für das Online-Skript zusätzlich:

```python
WP_URL      = "https://deine-wordpress-seite.de/wp-json/wp/v2"
WP_USER     = "dein-benutzername"
WP_PASSWORD = "dein-anwendungspasswort"
```

Das WordPress App-Passwort wird unter
Benutzer → Profil → Anwendungspasswörter generiert.

---

## Abhängigkeiten

```bash
pip install requests beautifulsoup4
```

Lokale DITA-OT-Installation unter `C:\DITA\dita-ot-4.4` und
portables Java 17 unter `C:\DITA\java25` werden vorausgesetzt.

---

## Konzeptioneller Hintergrund

Der Workflow demonstriert Single-Source-Publishing in der Praxis:

- **Eine Quelle** – DITA-Topics im XML-Format
- **Drei Ausgaben** – PDF, HTML5, WordPress
- **Automatisiert** – kein manueller Eingriff zwischen
  Authoring und Publishing
- **Versionierungssicher** – Slug-basierter Abgleich verhindert
  Duplikate bei Reimport
- **Hierarchietreu** – Parent-Child-Struktur aus der Ditamap
  wird in WordPress-Seitenhierarchie überführt

Dieses Prinzip – Content einmal erstellen, mehrfach und
medienneutral ausgeben – ist die Kernlogik hinter modernen
CCMS-Implementierungen mit Schema ST4, COSIMA oder vergleichbaren
Systemen. Der Workflow bildet diese Logik auf einem kleineren
Maßstab nach und macht sie praktisch erfahrbar.

---

## Lernkontext

Entwickelt im Rahmen der IHK-Weiterbildung
**Technische/-r Redakteur/-in (IHK)** beim IBB Institut für
Berufliche Bildung, Recklinghausen (Januar–September 2026).

Praktisches Begleitprojekt zur Vertiefung von:
- DITA-Strukturierung und Topic-based Writing
- DITA-OT-Build-Prozessen und Fehlerdiagnose
- Single-Source-Publishing-Konzepten
- Automatisierung von Dokumentationsprozessen
- WordPress REST API