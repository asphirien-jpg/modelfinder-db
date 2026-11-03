# Veröffentlichungsstatus – Magic Image Suite

**Stand:** 03.11.2026  
**Repository/Branch:** `asphirien-jpg/modelfinder-db`, `main`  
**Funktionsbasis zum Audit (vor diesem Dokumentations-Commit):** `eefff0ab9dda65c19ec9e16f3a55b5e84bf3565e`  
**Veröffentlichte Suite:** **v5.7.2**

Dieses Repository ist die veröffentlichte Update- und Datenquelle. Der
Quellcode- und Entwicklungsstatus wird zusätzlich im Repository
[`HardwareCheck_DEV`](https://github.com/asphirien-jpg/HardwareCheck_DEV)
geführt. Lokale Testdateien oder nicht eingecheckte Änderungen gehören nicht
automatisch zu einer Veröffentlichung.

## Bestätigt veröffentlicht

- Suite v5.7.2 über `latest_hardwarecheck_v5.json`, einschließlich der
  zusätzlichen Dell-/SATA-NTFS-Prüfung nach Clonezilla-Restore.
- Optionaler TreiberTrainer: lokale Schema-5-Lernpläne unter
  `#driver-coach/<Config>/driver-plan.json`; `#configs` bleibt frei von
  Lernplänen.
- Versionierte Medien-Ergänzung für den Windows-USB-Schutz unter
  [`media/windows-usb-protection`](media/windows-usb-protection).

## Präzisierung zum USB-Abschluss

Der Schutz entfernt zu Beginn nur Laufwerkszugriffspfade der drei
Boot-/Systemvolumes (`MISODEBIAN`, `ACRONIS`, `MISOLOBOOT`) auf derselben
USB-SSD. `MISOLOIMAGES` bleibt während Treiber-/Config-Abschluss verfügbar.
Am Ende wird **MISOLOIMAGES** nur nach erfolgreicher Label-Prüfung mit
`mountvol <Laufwerk>:\\ /p` ausgehängt. Der Erfolgshinweis bezieht sich daher
auf das getrennte Datenvolume, nicht auf eine zugesicherte physische Auswurf-
Operation der gesamten USB-SSD. Bei Fehlern zeigt das Skript eine Warnung und
empfiehlt, die SSD nicht sofort abzuziehen.

## Praxisstatus und Grenzen

- TreiberTrainer- und USB-Abschluss-Abläufe wurden auf realen Testgeräten
  geprüft. Einzelne gemessene Zeitgewinne sind Praxisbeobachtungen, keine
  Leistungszusage für jedes Modell oder jeden Treiberbestand.
- Der RAM-Test ist experimentell und nicht Teil der freigegebenen Suite v5.7.2.
- Frühere RAW-/Reparaturfälle sind nicht abschließend ursächlich erklärt.
  Erfolgreiche „Healthy“-Anzeigen nach Tests sind ein positives Ergebnis, aber
  kein Beweis für eine allgemeine Fehlerursache oder -freiheit.

Weitere Bedienhinweise, einschließlich Updateverhalten, stehen in
[MAGIC_IMAGE_SSD_README.md](MAGIC_IMAGE_SSD_README.md).
