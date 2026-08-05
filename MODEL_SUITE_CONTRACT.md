# ModelSuite Contract

Gilt fuer: `ModelFinder_DEV`, `HardwareCheck_DEV`, `modelfinder-db`, `hardwarecheck-status`, `Debian_DEV`.

## Zweck

Diese Repos bilden gemeinsam die ModelSuite:

- `ModelFinder_DEV`: Windows-Admin-/Suchtool, DB-Verwaltung, Statusuebersicht, HardwareCheck-Stick-Registrierung.
- `HardwareCheck_DEV`: Debian-Live-/Werkstatttool fuer Hardware-Erkennung, Reports, DB-/Programmupdate-Hinweise und Statusmeldung.
- `modelfinder-db`: zentrale Update-/Datenquelle fuer `model.json`, `model_manifest.json`, `latest_modelfinder.json`, `latest_hardwarecheck.json` und Updatepakete.
- `hardwarecheck-status`: Statusdateien von ModelFinder-PCs und HardwareCheck-Sticks.
- `Debian_DEV`: Debian-Live-Stick-/Installer-/Release-Vorlagen fuer HardwareCheck.

## Gemeinsame Datenbank-Regel

`modelfinder-db/model.json` ist die einzige gemeinsame Modelldatenbank. ModelFinder und HardwareCheck muessen dieselbe Datei ueber GitHub beziehen.

Wichtig:

- ModelFinder darf `model.json` verwalten und veroeffentlichen.
- HardwareCheck liest dieselbe `model.json` fuer Modellabgleich und DB-Updates.
- Keine zweite produktive Modelldatenbank in `HardwareCheck_DEV`, `ModelFinder_DEV` oder lokalen Testordnern einfuehren.
- Schema-Aenderungen zuerst hier dokumentieren, danach in beiden Tools kompatibel umsetzen.
- Neue Felder muessen alte Tools tolerieren koennen. Bestehende Felder duerfen nicht still umbenannt oder entfernt werden.

## Aktuelle Wahrheit

Die aktuellen Versions- und Datenbankstaende stehen zuerst in `modelfinder-db`:

- `model_manifest.json`
- `latest_modelfinder.json`
- `latest_hardwarecheck.json`
- `latest_hardwarecheck_v5.json`

Stand beim letzten Vertragsupdate: 2026-08-05

- DB: `2026.08.05.2`
- ModelFinder: `V4.41`
- HardwareCheck: `v5.0`
- HardwareCheck-Migration: `v3.78` -> `v4.99` (Bruecke) -> `v5.0`

Handover-Dateien in anderen Repos koennen aelter sein. Wenn sie abweichen, gilt zuerst das Manifest in `modelfinder-db`; danach die jeweilige Source-Version pruefen.

## Schnittstellen

### Modelldatenbank

`model_manifest.json` muss zu `model.json` passen:

- `version`
- `models_count`
- `sha256`
- `source_sha256`
- `canonical_sha256`
- `local_file_sha256`
- `updated_at`
- `database_file`
- `database_url`

Hash-Bedeutung:

- `sha256` / `source_sha256`: Hash der GitHub-Rohdatei, so wie Updater sie herunterladen.
- `canonical_sha256`: Hash der normalisierten JSON-Daten; stabiler gegen Formatierungsunterschiede.
- `local_file_sha256`: Hash der lokal geschriebenen Datei; kann wegen Zeilenenden vom GitHub-Rohhash abweichen.

Aenderungen an `model.json` muessen das Manifest aktualisieren. Vor Upload oder Release ausfuehren:

```powershell
python tools\verify_release_state.py
```

### Modelldaten-Schema

Consumer sollen unbekannte Felder ignorieren und bekannte Felder tolerant lesen.

Wichtige aktuelle Felder:

- `model_id`
- `product_number`
- `product_number_2`
- `manufacturer`
- `cpu`
- `onboard_ram_gb`
- `slot1_ram_gb`
- `slot2_ram_gb`
- `total_ram_gb`
- `ram_type`
- `ram_layout`
- `ssd_gb`
- `storage_type`
- `storage2_gb`
- `storage2_type`
- `drive`
- `screen_size`
- `display`
- `os`
- `keyboard`
- `condition`
- `color`
- `info`
- `software`
- `note`

`info` wird fuer Hinweise wie `Config` oder `Image` genutzt. `software` kann z. B. Office- oder Acronis-Hinweise enthalten.

### Programmupdates

`latest_modelfinder.json`, `latest_hardwarecheck.json` und
`latest_hardwarecheck_v5.json` muessen enthalten:

- `manifest_version`
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

HardwareCheck verwendet ab v5 zwei getrennte Manifestpfade:

- `latest_hardwarecheck.json` bleibt auf der Ein-Datei-Bruecke `v4.99`, damit
  alte v3.78-Sticks auch spaeter noch die erweiterte Allowlist erhalten.
- Bruecke und v5 lesen `latest_hardwarecheck_v5.json`. Dieses Manifest liefert
  v5.0 und alle kuenftigen v5-Programmupdates aus.

Die Bruecke darf nur `hardwarecheck_fast_gui.py` ersetzen. Erst danach darf das
v5-Paket zusaetzlich `hardwarecheck_v5_gui.py` installieren. Lokale Daten bleiben
in beiden Manifesten unter `preserve_paths` geschuetzt.

### Updatepakete

ZIPs unter `updates/` sind Updatepakete, keine Arbeitskopien. Sie duerfen nicht geloescht werden, solange alte Tools noch direkt auf diese Pfade aktualisieren.

Langfristige Regel:

- Alte Pakete erst entfernen oder auslagern, wenn ModelFinder und HardwareCheck eine Retention-/Release-Asset-Strategie unterstuetzen.
- Grosse ModelFinder-ZIPs moeglichst nicht weiter unendlich im Git-Repo ansammeln.
- Vor dem Entfernen alter ZIPs pruefen, welche Versionen noch im Umlauf sind.

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

ModelFinder-Status:

- ModelFinder speichert seinen Status-Token pro Windows-PC geschuetzt in der lokalen ModelFinder-Konfiguration.
- Ein kopierter ModelFinder kann einen geschuetzten Token von einem anderen PC nicht verlaesslich wiederverwenden.
- Wenn kein lokaler ModelFinder-Status-Token vorhanden ist, darf ModelFinder den Low-Scope-Token eines eingesteckten registrierten HardwareCheck-Sticks aus `hardwarecheck-status-token.txt` fuer die eigene Statusmeldung verwenden.
- Dadurch koennen HardwareCheck und ModelFinder auf Mitarbeiter-PCs sichtbar werden, ohne den Admin-/Publisher-Token zu verteilen.

### Debian Live

`Debian_DEV` darf HardwareCheck-Versionen nicht erraten. Es muss die stabile Source aus `HardwareCheck_DEV` und/oder das aktuelle Manifest aus `modelfinder-db` pruefen.

## Codex-Regeln

- Vor Arbeiten an einem ModelSuite-Repo diese Datei lesen.
- Vor Arbeiten an HardwareCheck/ModelFinder zuerst `modelfinder-db` aktualisieren und die Manifeste pruefen.
- Versionsupdates immer in Source, Manifest und Doku synchron halten.
- Statusschema nicht still brechen; kompatible Erweiterungen muessen hier dokumentiert werden.
- Token-Regeln nicht aufweichen.
- Bei UI-Aenderungen keine Update-/Statuslogik nebenbei veraendern.
- Nach DB-/Release-Aenderungen `tools\verify_release_state.py` ausfuehren.
