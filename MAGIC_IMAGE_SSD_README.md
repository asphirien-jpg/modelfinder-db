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

Der TreiberTrainer ist eine optionale Testfunktion und ersetzt das Original-Treiberskript nicht. Nach einem erfolgreichen Durchlauf kann er je Config einen Lernplan in `#configs/<Config>/driver-plan-test.json` ablegen. Beim nächsten gleichen Gerät werden bewährte INF-Treiber zuerst gezielt versucht. Anschließend läuft immer das unveränderte Originalskript als Sicherheitsnachlauf.

Dadurch bleiben neue oder geänderte Hardware sowie offene Geräte durch den Originalablauf abgesichert. Eine allgemeine Live-Freigabe erfolgt erst nach Zustimmung des ursprünglichen Programmierers und weiteren Tests.

## Medienaufbau

Nach der kleinen Programm-/Config-Basis werden vom Master nur ergänzt:

1. der vollständige Ordner `Treiber`;
2. die benötigten Clonezilla-Image-Ordner im Wurzelverzeichnis der Images-Partition.

Nicht übernehmen: alte Programmbackups, Windows-Papierkorb, Systemordner oder frühere Testskripte.
