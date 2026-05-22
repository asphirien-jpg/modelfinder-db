# ModelSuite Contract

Gilt fuer: `ModelFinder_DEV`, `HardwareCheck_DEV`, `modelfinder-db`, `hardwarecheck-status`, `Debian_DEV`.

## Zweck

Diese Repos bilden gemeinsam die ModelSuite:

- `ModelFinder_DEV`: Windows-Admin-/Suchtool, DB-Verwaltung, Statusuebersicht, HardwareCheck-Stick-Registrierung.
- `HardwareCheck_DEV`: Debian-Live-/Werkstatttool fuer Hardware-Erkennung, Reports, DB-/Programmupdate-Hinweise und Statusmeldung.
- `modelfinder-db`: zentrale Update-/Datenquelle fuer `model.json`, `model_manifest.json`, `latest_modelfinder.json`, `latest_hardwarecheck.json` und Updatepakete.
- `hardwarecheck-status`: Statusdateien von ModelFinder-PCs und HardwareCheck-Sticks.
- `Debian_DEV`: Debian-Live-Stick-/Installer-/Release-Vorlagen fuer HardwareCheck.

## Aktuelle Wahrheit

Die aktuellen Versions- und Datenbankstaende stehen zuerst in `modelfinder-db`:

- `model_manifest.json`
- `latest_modelfinder.json`
- `latest_hardwarecheck.json`

Handover-Dateien in anderen Repos koennen aelter sein. Wenn sie abweichen, gilt zuerst das Manifest in `modelfinder-db`; danach die jeweilige Source-Version pruefen.

## Schnittstellen

### Modelldatenbank

`model_manifest.json` muss zu `model.json` passen:

- `version`
- `models_count`
- `sha256`
- `updated_at`
- `database_url`

Aenderungen an `model.json` muessen das Manifest aktualisieren.

### Programmupdates

`latest_modelfinder.json` und `latest_hardwarecheck.json` muessen enthalten:

- `app`
- `version`
- `platform`
- `package_type`
- `download_url`
- `sha256`
- `size_bytes`
- `filename`
- `repo_path`
- `created_at`
- `notes`

SHA256 und Groesse muessen zum hochgeladenen ZIP passen.

### HardwareCheck-Stick-Registrierung

ModelFinder darf auf einen HardwareCheck-Stick schreiben:

- `device_identity.json`
- optional `hardwarecheck-status-token.txt`

HardwareCheck liest diese Dateien und meldet Status.

### Statusmeldungen

Statusdateien liegen in:

```text
hardwarecheck-status/status/<device_id>.json
```

Neue Implementierungen sollen die kanonischen Feldnamen schreiben. Bestehende Tools duerfen die genannten kompatiblen Alias-Felder weiter liefern; Consumer muessen beide Formen lesen, damit alte Sticks/portable ModelFinder-Installationen nicht brechen.

Erwartete Felder:

- `device_id`
- Anzeigename: `display_name`, `employee_name` oder `device_name`
- `tool`
- `app_version`
- `db_version`
- Modellanzahl: kanonisch `db_model_count`, kompatibel auch `db_models_count`
- `event`
- Zeitstempel: kanonisch `last_seen`, kompatibel auch `last_seen_utc`
- optional Updatehinweise: `hint`, `update_state`, `program_message`, `db_message`
- optional ModelFinder-Scope: `portable_device_id`, `local_profile`, `status_scope`

Status-Tokens muessen Low-Scope-Tokens sein. Niemals den Admin-/Publisher-Token auf Mitarbeitersticks speichern.

Aktueller Implementierungsstand ab 2026-05-22:

- HardwareCheck `v3.61` schreibt `db_model_count` und `last_seen` plus `db_models_count` und `last_seen_utc`.
- ModelFinder `V4.21` schreibt fuer eigene Statusmeldungen dieselben kanonischen Felder plus Aliase.
- ModelFinder `V4.21` liest `last_seen` oder `last_seen_utc` sowie `hint`, `update_state`, `program_message` oder `db_message`.

### Debian Live

`Debian_DEV` darf HardwareCheck-Versionen nicht erraten. Es muss die stabile Source aus `HardwareCheck_DEV` und/oder das aktuelle Manifest aus `modelfinder-db` pruefen.

## Codex-Regeln

- Vor Arbeiten an einem ModelSuite-Repo diese Datei lesen.
- Versionsupdates immer in Source, Manifest und Doku synchron halten.
- Statusschema nicht still brechen; kompatible Erweiterungen muessen hier dokumentiert werden.
- Token-Regeln nicht aufweichen.
- Bei UI-Aenderungen keine Update-/Statuslogik nebenbei veraendern.
- Nach Aenderungen `TASKS_NEXT.md` und relevante Handover-Dateien aktualisieren.
