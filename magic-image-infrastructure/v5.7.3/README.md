# Magic Image Infrastruktur – v5.7.3

Diese Dateien sind die **Referenz für die SSD-Grundstruktur**, nicht ein normales Programmupdate.

## Enthalten

| Datei | Zielort / Zweck |
| --- | --- |
| `runtime_bootstrap.py` | Kleine statische Startbrücke auf `D:\HardwareCheck\hardwarecheck_fast_gui.py` |
| `Hide-MagicImage-SystemVolumes.ps1` | Windows-Handoff: blendet D/E/G derselben USB-SSD nur für die aktuelle Sitzung aus |
| `Finalize-MagicImage-USB.ps1` | Windows-Handoff: versucht am Ende, `MISOLOIMAGES` sicher zu trennen |

## Wichtig

- Normale v5.7.3-Updates liefern die App-Dateien. Sie dürfen diese Brücke **nicht**
  ersetzen und dürfen `F:\HardwareCheck-Runtime` nicht überschreiben.
- `F:\HardwareCheck-Runtime` enthält die vollständigen GUIs sowie lokale
  Einstellungen, Logs und Zustände. Sie ist bewusst **kein** allgemeiner
  FreeFileSync-Inhalt.
- Für eine migrierte Anwender-SSD müssen auf D: neben der kleinen Brücke auch
  `hardwarecheck_fast_gui.recovery.py` als vollständiger Notfall-Fallback
  vorhanden sein. Der Recovery-Quellstand kommt aus dem geprüften Suite-Paket,
  nicht aus dieser Infrastrukturablage.
- Die vier Partitionen werden weder von diesen Dateien noch von einem
  normalen Programmupdate erzeugt oder verändert.

## Geprüfte SHA-256-Referenzen (13.11.2026)

- `runtime_bootstrap.py`: `FE37352ECF5A5E1278AE533CB4AC753EF8DE700A456888EE7217BBA63AB0236E`
- `Hide-MagicImage-SystemVolumes.ps1`: `7B2C2EAAA0B948AF70BC8F0965FB0314843662213C513E1A15B3AD48167876DD`
- `Finalize-MagicImage-USB.ps1`: `963755813B01767A23F6B08D3690461ECC3D197EB1FB66801BB1669AE7005643`

Die Gesamtarchitektur, Grenzen und Rollout-Regeln stehen in
`docs/MAGIC_IMAGE_GESAMTUEBERGABE.md`.
