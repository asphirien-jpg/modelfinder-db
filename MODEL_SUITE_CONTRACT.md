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

Erwartete Felder:

- `device_id`
- `display_name` oder `employee_name`
- `tool`
- `app_version`
- `db_version`
- `db_model_count`
- `event`
- `last_seen`
- optional `hint` / `update_state`

Status-Tokens muessen Low-Scope-Tokens sein. Niemals den Admin-/Publisher-Token auf Mitarbeitersticks speichern.

### Debian Live

`Debian_DEV` darf HardwareCheck-Versionen nicht erraten. Es muss die stabile Source aus `HardwareCheck_DEV` und/oder das aktuelle Manifest aus `modelfinder-db` pruefen.

## Codex-Regeln

- Vor Arbeiten an einem ModelSuite-Repo diese Datei lesen.
- Versionsupdates immer in Source, Manifest und Doku synchron halten.
- Statusschema nicht still brechen.
- Token-Regeln nicht aufweichen.
- Bei UI-Aenderungen keine Update-/Statuslogik nebenbei veraendern.
- Nach Aenderungen `TASKS_NEXT.md` und relevante Handover-Dateien aktualisieren.
