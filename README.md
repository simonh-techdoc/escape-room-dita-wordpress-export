# DITA-Projekt „Escape Room“

Dieses Repository enthält ein exemplarisches DITA-Dokumentationsprojekt zum Thema **Escape Room**. Es demonstriert Topic-based Writing, Wiederverwendung über Keys und Single-Source-Publishing aus einer gemeinsamen XML-Quelle in mehrere Ausgabeformate.

Das Projekt ist als praxisnahes Lern- und Portfolio-Projekt für Technische Redaktion angelegt. Es zeigt, wie strukturierte Inhalte in DITA modelliert, mit DITA-OT verarbeitet und anschließend als HTML, PDF und WordPress-taugliche Ausgabe bereitgestellt werden können.

## Projektziel

Ziel des Projekts ist es, einen kleinen, aber vollständigen Dokumentationsworkflow abzubilden:

- strukturierte Inhaltserstellung mit DITA-Topics
- zentrale Steuerung über eine DITA-Map
- Wiederverwendung variabler Inhalte über Keyrefs
- automatische Ausgabe als HTML5 und PDF
- Weiterverarbeitung des HTML-Outputs für WordPress

Damit bildet das Projekt im kleinen Maßstab typische Konzepte moderner Component-Content-Management-Systeme ab: medienneutrale Quellen, modulare Topics, Single Source of Truth und automatisierte Publikation.

## Inhaltliches Szenario

Die Beispielinhalte beschreiben einen Escape-Room-Guide. Die Dokumentation richtet sich an Nutzerinnen und Nutzer, die verstehen möchten, wie das Angebot funktioniert und wie sie ein Team anmelden bzw. starten können.

Die Inhalte sind bewusst überschaubar gehalten, damit die technische Struktur des DITA-Projekts gut nachvollziehbar bleibt.

## DITA-Struktur

```text
maps/
├── main.ditamap      # Hauptmap mit Publikationsstruktur
└── keys.ditamap      # zentrale Key-Definitionen

topics/
├── overview.dita     # Überblick / Concept
├── how-it-works.dita # Ablaufbeschreibung / Task
└── cta.dita          # Handlungsaufforderung / Task

components/
├── team-info.dita    # wiederverwendbarer Inhaltsbaustein
└── timing.dita       # wiederverwendbarer Inhaltsbaustein
```

Die `main.ditamap` definiert die Reihenfolge und Publikationsstruktur der Topics. Die `keys.ditamap` enthält zentrale Variablen bzw. wiederverwendbare Werte, die über `keyref` in den Topics referenziert werden.

## Informationsarchitektur

Die Topic-Typen folgen dem DITA-Grundprinzip der funktionalen Trennung:
Concept-Topics beschreiben **Was** – sie liefern Kontext und Überblick.
Task-Topics beschreiben **Wie** – sie führen durch konkrete Handlungsschritte.
Diese Trennung ist keine Konvention, sondern eine bewusste
informationsarchitektonische Entscheidung: Sie ermöglicht gezielte
Wiederverwendung einzelner Bausteine ohne inhaltliche Abhängigkeiten.

Die `keys.ditamap` separiert variable Inhalte – Produktnamen, Zeitangaben –
von der stabilen Dokumentationsstruktur. Eine Änderung am Key propagiert
automatisch in alle Verwendungsstellen aller Ausgabeformate. Das ist
Single Source of Truth auf Komponentenebene.

Die Parent-Child-Hierarchie der DITA-Map wird im WordPress-Export als
Seitenhierarchie abgebildet – Content-Struktur und Ausgabestruktur bleiben
konsistent. Wer die Map verändert, verändert gleichzeitig die
Navigationsstruktur der Website.

## Ausgabeformate

Das Projekt enthält bereits erzeugte Beispieloutputs:

```text
output-html/       # HTML5-Ausgabe aus DITA-OT
output-pdf/        # PDF-Ausgabe aus DITA-OT
output-wordpress/  # HTML-Ausgabe für WordPress-Weiterverarbeitung
```

Die Outputs dienen als nachvollziehbarer Nachweis des Publishing-Prozesses. Die eigentliche Quelle bleiben jedoch die DITA-Dateien in `topics/`, `components/` und `maps/`.

## Build-Prozess

Der Build wird über das Batch-Skript gestartet:

```bat
DITA-build-HTML+PDF.bat
```

Das Skript erzeugt HTML- und PDF-Ausgaben aus der DITA-Map. Vorausgesetzt werden eine lokale DITA-OT-Installation und eine passende Java-Laufzeitumgebung gemäß Projektkonfiguration.

## WordPress-Export

Zusätzlich enthält das Projekt zwei Python-Skripte für die WordPress-Ausgabe:

```text
wordpress-push-offline.py # lokale Bereinigung und Prüfung der WordPress-Ausgabe
wordpress-push-online.py  # Push zu WordPress über REST API
```

Das Online-Skript nutzt die WordPress REST API und arbeitet slug-basiert. Bestehende Seiten werden aktualisiert, neue Seiten werden angelegt. Die Hierarchie kann aus der DITA-Map abgeleitet und auf WordPress-Seiten übertragen werden.

Die technische Dokumentation dieses Export-Workflows steht in der bestehenden `README.md`.

## Technischer Kontext

| Bereich | Umsetzung |
|---|---|
| Authoring | DITA 1.3 / XML |
| Strukturierung | DITA-Map, Topics, Keyrefs |
| Build | DITA Open Toolkit |
| Ausgabe | HTML5, PDF, WordPress-HTML |
| Automatisierung | Windows Batch, Python |
| WordPress-Anbindung | REST API v2 |

## Lern- und Demonstrationswert

Das Projekt zeigt insbesondere:

- Trennung von Inhalt, Struktur und Ausgabe
- konsequente modulare Dokumentation
- medienneutrales Schreiben mit DITA
- Automatisierung von Publishing-Prozessen
- Übertragung strukturierter Technischer Dokumentation in ein Web-CMS

Es eignet sich damit als Demonstrator für Technische Redaktion, XML-basierte Dokumentation, Single-Source-Publishing und einfache CCMS-nahe Workflows.

## Hinweise

Die erzeugten Output-Ordner sind im Repository enthalten, damit der komplette Demonstrationsstand nachvollziehbar bleibt. Für produktive Projekte würde man generierte Outputs häufig nicht versionieren, sondern über Build- oder CI-Prozesse erzeugen lassen.

