# Magic Image Infrastruktur – v5.7.4

## Freigabeumfang

v5.7.4 verlegt den temporären Magic-Image-Handoff von `C:\MagicImage` nach
`C:\Windows\Addins\MagicImage`.

- Die Linux-Runtime sucht den **bereits vorhandenen** Addins-Ordner
  schreibweisenunabhängig und bricht sicher ab, wenn dieser fehlt oder doppelt
  vorhanden ist. Sie erzeugt nie einen zweiten `Addins`-/`addins`-Ordner.
- Der Windows-Abschluss liest denselben Pfad und entfernt nach erfolgreicher
  Installation ausschließlich den Unterordner `MagicImage`.
- Kein Update dieser Version löscht oder ersetzt Inhalte von
  `C:\Windows\Addins` außerhalb dieses temporären Unterordners.

## Rollout

Das GitHub-Suitepaket aktualisiert die Programm-Runtime. Für bereits vorhandene
Anwender-SSDs muss zusätzlich der kontrollierte Medien-Updater aus dem
4-Partitionen-Ersteller verwendet werden, weil nur dieser auch
`image-deploy.bat` auf der Images-Partition aktualisiert.

Der Medien-Updater darf ausschließlich Runtime-/Handoff-Dateien einschließlich
`image-deploy.bat` und – wenn vorhanden – den TreiberTrainer ändern. Images,
Treiber, Configs, Partitionen, Kundengeräte und der separate Runtime-Boot-
Langzeittest bleiben unverändert.

Die Funktion wurde vor der Freigabe auf einer Anwender-Test-SSD mit vollständiger
Installation erfolgreich geprüft.
