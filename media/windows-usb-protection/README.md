# Windows USB-Abschluss-Schutz

Stand: **getestet am 30.10.2026**

Diese Medien-Ergänzung schützt die Magic-Image-USB-SSD während und nach dem
Windows-Abschluss vor unnötigen Schreibzugriffen. Sie ist **kein** normales
HardwareCheck-Programmupdate: Die Dateien gehören auf die große Datenpartition
`MISOLOIMAGES` der jeweiligen Anwender-SSD.

## Zweck

Während Windows die Treiber und die Config abschließt, werden nur die
Zugriffspfade der drei Boot-/Systempartitionen derselben USB-SSD entfernt:

- `MISODEBIAN`
- `ACRONIS`
- `MISOLOBOOT`

`MISOLOIMAGES` bleibt für Treiber, Configs und den normalen Abschluss verfügbar.
Es werden dabei keine GPT-Attribute, Partitionen oder Dateisysteme verändert.

Nach einem erfolgreichen Abschluss wird der Handoff-Ordner `C:\MagicImage`
gelöscht. Ein lokaler, kurz verzögerter Abschlussprozess trennt anschließend
auch `MISOLOIMAGES` per `mountvol /p` sauber und zeigt eine deutsche/tschechische
Bestätigung an. Bei einem Fehler bleibt die SSD sichtbar und es erscheint eine
Warnung, sie noch nicht abzuziehen.

Das reduziert das Risiko von FAT32-`RAW`-Zuständen nach vorschnellem Abziehen.
Es ersetzt nicht die übliche Sorgfalt beim Abziehen, verändert aber keine
Kundendatenträger außerhalb der erkannten Magic-Image-SSD.

## Dateien auf `MISOLOIMAGES`

Folgende drei Dateien werden zusammen installiert bzw. aktualisiert:

1. `image-deploy.bat` – startet den Schutz und den Abschluss.
2. `Hide-MagicImage-SystemVolumes.ps1` – entfernt für die laufende
   Windows-Sitzung ausschließlich die Zugriffspfade von D/E/G derselben SSD.
3. `Finalize-MagicImage-USB.ps1` – trennt nach erfolgreichem Abschluss F:
   sauber und zeigt die Abschlussmeldung.

Die beiden PowerShell-Dateien liegen in diesem Ordner. Die getestete Änderung
an `image-deploy.bat` wird als Medien-Patch in der SSD-Aufbau-Dokumentation
referenziert, damit Programm-Updates nicht versehentlich Medien-Dateien
überschreiben.

## Rollout

Bestehende SSDs werden kontrolliert einzeln aktualisiert und anschließend per
SHA-256 geprüft. Ein zukünftiger SSD-Ersteller soll diese drei Dateien beim
Medienaufbau direkt auf `MISOLOIMAGES` übernehmen.
