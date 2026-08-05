# modelfinder-db

Dieses Repo ist die gemeinsame Update- und Datenquelle fuer die ModelSuite.

## Gemeinsame Wahrheit

`model.json` ist die zentrale Modelldatenbank fuer:

- ModelFinder
- HardwareCheck

Beide Tools duerfen lokal Kopien nutzen, aber die veroeffentlichte Wahrheit liegt hier im Repo. Wenn ModelFinder Daten aendert und hochlaedt, muessen `model.json` und `model_manifest.json` gemeinsam aktualisiert werden. HardwareCheck darf diese Datei lesen, aber keine eigene abweichende Modelldatenbank pflegen.

## Wichtige Dateien

- `model.json`: gemeinsame Modelldatenbank.
- `model_manifest.json`: Version, Modellanzahl und Hashes der Modelldatenbank.
- `latest_modelfinder.json`: aktuelles ModelFinder-Programmpaket.
- `latest_hardwarecheck.json`: dauerhafte Kompatibilitaetsbruecke fuer bestehende
  HardwareCheck-v3.78-Sticks.
- `latest_hardwarecheck_v5.json`: aktuelles HardwareCheck-v5-Programmpaket.
- `updates/modelfinder/`: ModelFinder-Update-ZIPs.
- `updates/hardwarecheck/`: HardwareCheck-Update-ZIPs.
- `MODEL_SUITE_CONTRACT.md`: Schnittstellenvertrag fuer alle beteiligten Repos.

## Vor jedem Release pruefen

```powershell
python tools\verify_release_state.py
```

Optional mit GitHub-Rohdateien:

```powershell
python tools\verify_release_state.py --remote
```

Der Pruefer bricht bei echten Fehlern ab und warnt nur bei Repo-Ballast wie vielen ZIP-Dateien oder grossen Paketen.

## Updatepakete und "Backups"

Die ZIP-Dateien unter `updates/` sind keine klassischen Backups, sondern Updatepakete fuer bereits verteilte ModelFinder- und HardwareCheck-Versionen. Sie sollten nicht geloescht werden, solange alte Tools noch direkt auf diese Dateien aktualisieren koennen.

Langfristig ist das Repo aber bereits gross genug, dass wir eine Retention-Regel oder GitHub-Releases vorbereiten sollten. Erst wenn die Updater alte Paketpfade nicht mehr brauchen, duerfen alte ZIPs entfernt oder ausgelagert werden.
