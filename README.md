# DITA-Projekt „Escape Room"

Dieses Repository enthält ein exemplarisches DITA-Dokumentationsprojekt zum Thema **Escape Room**. Es demonstriert Topic-based Writing, Wiederverwendung über Keys und Single-Source-Publishing aus einer gemeinsamen XML-Quelle in mehrere Ausgabeformate.

Das Projekt ist als praxisnahes Lern- und Portfolio-Projekt für Technische Redaktion angelegt. Es zeigt, wie strukturierte Inhalte in DITA modelliert, mit DITA-OT verarbeitet und anschließend als HTML, PDF und WordPress-taugliche Ausgabe bereitgestellt werden können.

Das Thema „Escape Room" dient dabei primär als neutraler Demonstrator für strukturierte Informationsarchitektur, modulare Content-Modellierung und automatisierte Publishing-Workflows. Die zugrunde liegenden Konzepte wären ebenso auf Produktdokumentation, Wissensdatenbanken oder andere dokumentationsorientierte Systeme übertragbar.

---

## Projektziel

Ziel des Projekts ist es, einen kleinen, aber vollständigen Dokumentationsworkflow abzubilden:

- strukturierte Inhaltserstellung mit DITA-Topics
- zentrale Steuerung über eine DITA-Map
- Wiederverwendung variabler Inhalte über Keyrefs
- automatische Ausgabe als HTML5 und PDF
- Weiterverarbeitung des HTML-Outputs für WordPress

Damit bildet das Projekt im kleinen Maßstab typische Konzepte moderner Component-Content-Management-Systeme ab:

- medienneutrale Quellen
- modulare Topics
- Single Source of Truth
- automatisierte Publikation
- Trennung von Inhalt, Struktur und Ausgabe

---

## Inhaltliches Szenario

Die Beispielinhalte beschreiben einen Escape-Room-Guide. Die Dokumentation richtet sich an Nutzerinnen und Nutzer, die verstehen möchten:

- wie das Angebot funktioniert
- wie ein Spiel vorbereitet wird
- wie ein Team startet
- welche organisatorischen Rahmenbedingungen gelten

Die Inhalte sind bewusst überschaubar gehalten, damit die technische Struktur des DITA-Projekts nachvollziehbar bleibt und der Fokus auf Informationsarchitektur und Publishing liegt.

---

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

Die `main.ditamap` definiert die Reihenfolge und Publikationsstruktur der Topics.

Die `keys.ditamap` enthält zentrale Variablen bzw. wiederverwendbare Werte, die über `keyref` in den Topics referenziert werden.

---

## Informationsarchitektur

Die Topic-Typen folgen dem DITA-Grundprinzip der funktionalen Trennung:

- Concept-Topics beschreiben **Was** – sie liefern Kontext und Überblick.
- Task-Topics beschreiben **Wie** – sie führen durch konkrete Handlungsschritte.

Diese Trennung ist keine reine Konvention, sondern eine bewusste informationsarchitektonische Entscheidung: Sie ermöglicht gezielte Wiederverwendung einzelner Bausteine ohne inhaltliche Abhängigkeiten.

Die `keys.ditamap` separiert variable Inhalte – beispielsweise Produktnamen oder Zeitangaben – von der stabilen Dokumentationsstruktur. Änderungen an zentralen Keys propagieren automatisch in alle Verwendungsstellen und Ausgabeformate.

Damit entsteht ein komponentenorientierter Single-Source-Ansatz.

Die Parent-Child-Hierarchie der DITA-Map wird im WordPress-Export zusätzlich als Seiten- bzw. Navigationsstruktur abgebildet. Dadurch bleiben Inhaltsstruktur und Ausgabestruktur konsistent:

> Wer die DITA-Map verändert, verändert gleichzeitig die Navigationsstruktur der Website.

---

## Publishing-Workflow

```text
DITA Topics
   ↓
DITA Map
   ↓
DITA Open Toolkit
   ↓
HTML5 / PDF / WordPress-HTML
   ↓
WordPress REST API
   ↓
WordPress-Seitenstruktur
```

Der Workflow demonstriert die Transformation strukturierter XML-Quellen in unterschiedliche Zielmedien aus einer gemeinsamen Content-Basis.

---

## Ausgabeformate

Das Projekt enthält bereits erzeugte Beispieloutputs:

```text
output-html/       # HTML5-Ausgabe aus DITA-OT
output-pdf/        # PDF-Ausgabe aus DITA-OT
output-wordpress/  # HTML-Ausgabe für WordPress-Weiterverarbeitung
```

Die Outputs dienen als nachvollziehbarer Nachweis des Publishing-Prozesses.

Die eigentliche Quelle bleiben jedoch ausschließlich die DITA-Dateien in:

- `topics/`
- `components/`
- `maps/`

---

## Build-Prozess

Der Build wird über das Batch-Skript gestartet:

```bat
DITA-build-HTML+PDF.bat
```

Das Skript erzeugt HTML- und PDF-Ausgaben aus der DITA-Map.

Vorausgesetzt werden:

- eine lokale DITA-OT-Installation
- eine passende Java-Laufzeitumgebung
- korrekt konfigurierte Umgebungsvariablen

---

## WordPress-Export

Zusätzlich enthält das Projekt zwei Python-Skripte für die WordPress-Ausgabe:

```text
wordpress-push-offline.py # lokale Bereinigung und Prüfung der WordPress-Ausgabe
wordpress-push-online.py  # Push zu WordPress über REST API
```

Die WordPress-Anbindung dient als ergänzender Demonstrator für die Weiterverarbeitung strukturierter Inhalte in einem Web-CMS.

Das Online-Skript nutzt die WordPress REST API und arbeitet slug-basiert:

- bestehende Seiten werden aktualisiert
- neue Seiten werden automatisch angelegt
- Seitenhierarchien können aus der DITA-Map übernommen werden

Dadurch lässt sich die strukturierte DITA-Architektur teilweise direkt in WordPress reproduzieren.

---

## Technischer Kontext

| Bereich | Umsetzung |
|---|---|
| Authoring | DITA 1.3 / XML |
| Strukturierung | DITA-Map, Topics, Keyrefs |
| Build | DITA Open Toolkit |
| Ausgabe | HTML5, PDF, WordPress-HTML |
| Automatisierung | Windows Batch, Python |
| WordPress-Anbindung | REST API v2 |
| Versionsverwaltung | Git / GitHub |

---

## Lern- und Demonstrationswert

Das Projekt demonstriert insbesondere:

- Trennung von Inhalt, Struktur und Ausgabe
- modulare Dokumentation mit Wiederverwendung
- medienneutrales Schreiben mit DITA
- komponentenorientierte Informationsarchitektur
- automatisierte Publishing-Prozesse
- Übertragung strukturierter Technischer Dokumentation in ein Web-CMS
- grundlegende CCMS-nahe Workflows im kleinen Maßstab

Es eignet sich damit als Demonstrator für:

- Technische Redaktion
- XML-basierte Dokumentation
- DITA-Grundlagen
- Single-Source-Publishing
- strukturierte Informationsarchitektur
- einfache Content-Engineering-Workflows

---

## Hinweise

Die erzeugten Output-Ordner sind im Repository enthalten, damit der vollständige Demonstrationsstand nachvollziehbar bleibt.

In produktiven Projekten würden generierte Outputs häufig nicht versioniert, sondern automatisiert über Build- oder CI/CD-Prozesse erzeugt werden.

Das Repository dient primär der Veranschaulichung von Strukturierungs-, Publishing- und Automatisierungskonzepten im Umfeld moderner Technischer Dokumentation.