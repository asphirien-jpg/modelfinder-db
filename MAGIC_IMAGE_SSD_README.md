# Magic Image – Installations-SSD

Stand: **v5.7.1**. Magic Image, HardwareCheck und CompactCheck verwenden den gemeinsamen freigegebenen Programmstand. Der SSD-Ersteller lädt vor jedem Aufbau das aktuelle GitHub-Manifest, prüft das Programmpaket per SHA-256 und kopiert diese aktuelle Dokumentation auf die Images-Partition.

## Ablauf

1. Magic Image starten, Gerätetyp und vierstellige Config wählen.
2. Abweichungen nur bei eindeutig passendem Gerät bewusst bestätigen.
3. Clonezilla-Image und interne Ziel-SSD auswählen, dann installieren.
4. Nach dem Windows-Start erfolgt der normale Treiber- und Sicherheitsabschluss.

Über das Zahnrad kann ohne PC-Neustart zwischen Magic Image, HardwareCheck und CompactCheck gewechselt werden. Images, Configs und Datenbank bleiben unverändert.

## USB-Geschwindigkeit

Die Oberfläche zeigt den Anschluss des Installationsmediums an. `USB 3.x SuperSpeed · 5000 Mbit/s` ist der normale schnelle Betrieb; `USB 2.0 High-Speed · 480 Mbit/s` kann Restore und Erkennung deutlich bremsen.

## Updates

Programm- und Datenbank-Updates sind getrennt. Das Programm lädt nur über das offizielle HTTPS-Manifest und akzeptiert Pakete erst nach SHA-256-Prüfung. Images, `#configs`, Treiber, WLAN-Profile und lokale Einstellungen werden nicht überschrieben.

## TreiberTrainer – Testfunktion, kein Live-Standard

Der TreiberTrainer ist eine optionale Testfunktion und ersetzt den bewährten ersten Originallauf nicht. Er lernt erst nach einem vollständig erfolgreichen Originallauf die von Windows tatsächlich gebundene Treiber-INF je Gerät (Windows-`oemXX.inf` plus konkreter INF-Pfad aus dem Originallog). Die Zuordnung wird als Schema-5-Plan in `#configs/<Config>/driver-plan-test.json` gespeichert.

Beim nächsten Gerät mit exakt passenden Hardware-IDs werden nur diese validierten INF-Dateien gezielt installiert. Derselbe vollständige INF-Pfad wird dabei innerhalb eines Durchlaufs nur einmal aufgerufen; Windows bindet das Paket anschließend an alle dazu passenden Geräte. Bleiben danach Geräte offen, ist der Plan ungültig, fehlt ein Pfad oder meldet die Installation einen Fehler, folgt das unveränderte Originalskript als Sicherheitsnachlauf. Sind alle Geräte nach dem gezielten Lauf versorgt, wird der zeitaufwändige Originallauf nicht erneut gestartet. Für Config 8567 ergab der Test am 20.03.2026 16:28 Minuten im ersten Lauf und 6:02 Minuten im validierten zweiten Lauf.

Dadurch bleiben neue oder geänderte Hardware sowie offene Geräte durch den Originalablauf abgesichert. Eine allgemeine Live-Freigabe erfolgt erst nach Zustimmung des ursprünglichen Programmierers und weiteren Tests.

## Medienaufbau

Nach der kleinen Programm-/Config-Basis werden vom Master nur ergänzt:

1. der vollständige Ordner `Treiber`;
2. die benötigten Clonezilla-Image-Ordner im Wurzelverzeichnis der Images-Partition.

Nicht übernehmen: alte Programmbackups, Windows-Papierkorb, Systemordner oder frühere Testskripte.
