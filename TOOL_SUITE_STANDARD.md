# Tool Suite Standard - Codex / ChatGPT Arbeitsregeln

Diese Datei ist die globale Arbeitsgrundlage fuer alle internen Tools in den asphirien-jpg Repositories.

## Grundsatz

Das jeweilige GitHub-Repository ist die Wahrheit. Ein Codex-Chat darf sich nicht nur auf Chatverlauf oder Erinnerung verlassen. Vor jeder Arbeit zuerst die Projektdateien im Repo lesen.

## Pflichtreihenfolge fuer jeden Codex-Chat

1. `CODEX_PROJECT_RULES.md` lesen, falls vorhanden.
2. `AGENTS.md`, `CODEX_START_HERE.md`, `CURRENT_STATE*.md` oder vorhandene Handover-Dateien lesen.
3. `TASKS_NEXT.md` lesen.
4. Bei verbundenen Tools die Suite-/Schnittstellenregeln im Projekt beachten.
5. Erst danach Code aendern.

## Allgemeine Regeln

- Keine echten Tokens, API-Keys, WLAN-Passwoerter, privaten Pfade, Kunden-/Serverdaten oder lokalen Configs committen.
- Keine generierten Reports, Backups, Build-Ausgaben, EXEs oder ZIPs committen, ausser das Repo ist explizit ein Release-/Update-Repo.
- Bestehende stabile Logik nicht nebenbei umbauen.
- Kleine, nachvollziehbare Aenderungen bevorzugen.
- Nach jeder Aenderung Version, Changelog, Status oder Aufgabenliste aktualisieren, wenn sich der Stand geaendert hat.
- Bei Fehlern Ursache dokumentieren statt nur Symptome zu kaschieren.
- Bei wichtigen Tools vor riskanten Schreibvorgaengen Backup-/Rollback-Verhalten pruefen.

## Tool-Gruppen

### ModelSuite

Repos: `ModelFinder_DEV`, `HardwareCheck_DEV`, `modelfinder-db`, `hardwarecheck-status`, `Debian_DEV`.

Gemeinsam regeln sie Modelldatenbank, Programmupdates, HardwareCheck-Sticks, Statusmeldungen und Debian-Live-Verteilung. Versions- und Manifestdaten muessen synchron bleiben.

### DriverSuite

Repos: `Magic-Image-Driver-Tool_DEV`, `DB-Updater_Dev`, `Cat-Folder-Factory_DEV`.

CAT Folder Factory erzeugt Treiberpakete, DB Updater ergaenzt vorhandene Treiberordner/Indexe, Magic Image Driver Tool installiert und verwaltet die Treiber im Magic-Image-Workflow.

### LabelSuite

Repos: `G2000-Label-Creator_DEV`, `Laptop-Box-Label-Creator_DEV`, `SSD-LabelCreator_DEV`.

Druckmasse, Barcode-Regeln, Layoutkorrektur und Druckkalibrierung sind fachkritisch. Aussenmasse nicht ohne Auftrag aendern.

### WorkflowSuite

Repos: `Delivery-Note-Creator_DEV`, `Reklamation-Note-Creator_DEV`.

Excel-, Import-, Export- und Workflowlogik muss mit Testdaten und Backups abgesichert werden.

### Translator

Repo: `czde-translator-api`.

API-Key, CORS, Auth, Rate-Limits und Kostenkontrolle sind sicherheitskritisch.

## Regel fuer zusammenhaengende Tools

Wenn ein Tool Dateien, JSON-Schemata, Update-Manifeste oder Statusdaten erzeugt, die ein anderes Tool liest, ist das eine Schnittstelle. Schnittstellen nicht still veraendern. Erst Contract lesen, dann Aenderung dokumentieren, dann betroffene Repos synchronisieren.
