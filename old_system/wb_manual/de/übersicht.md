[<< zurück](https://github.com/michel-abele/python-website-builder)

:de:

# Projektübersicht

Ich setze mir das Ziel, bis zur Veröffentlichung der Version 1.0 von PyWeB, folgende Inhalte und Funktionen bereitzustellen.

## Module

### Initiierung der Werkbank

Durch den Befehl `py wb.py init` oder die Kurzform `py wb.py i` wird das aktuelle Verzeichnis von vorhandenen Git-Repository-Verzeichnissen und Dateien bereinigt und zugleich werden die erforderlichen Verzeichnisse sowie Grunddateien für den Einsatz erstellt.

### Bau der Webseite

Mit dem Befehl `py wb.py build` oder der Kurzform `py wb.py b` wird der Aufbau der Webseite gestartet. Im Laufe dieses Prozesses erfolgt die Integration von Teildateien in die zentralen Dateien, das Einfügen von Variablen sowie die Bearbeitung weiterer anstehender Aufgaben.

#### Ablauf

1. Die erforderlichen Bibliotheksverzeichnisse (library) werden angelegt.
1. Die Synchronisation der HTML-Dateien erfolgt vom Quellverzeichnis zum Zielverzeichnis. Dabei werden leere Verzeichnisse und HTML-Dateien, die nicht länger im Quellverzeichnis vorhanden sind, aus dem Zielverzeichnis entfernt. Die Optionen `-clear` und die entsprechende Kurzoption `-c` pausieren die Synchronisation und führen zur Löschung aller Dateien sowie Verzeichnisse im Zielverzeichnis, was einen vollständigen Neuaufbau der Webseite zur Folge hat.
1. Es wird das temporäre Verzeichnis _./temp_ erstellt.
1. Die HTML-Dateien aus dem Quellverzeichnis werden verarbeitet.
    1. Die Änderungszeiten aller HTML-Teildateien werden überprüft und temporär gespeichert. Dies dient dazu, zu einem späteren Zeitpunkt die Aktualität der Hauptdatei bestimmen zu können.
    1. Es erfolgt eine Überprüfung, ob die Webseite einsprachig oder mehrsprachig gestaltet ist. Diese Information ist für die spätere Erstellung der XML-Sitemap-Dateien erforderlich.
    1. Alle Teildateien werden in die Hauptdateien eingefügt, wobei Teildateien wiederum weitere Teildateien enthalten können.
    1. Die unterschiedlichen Variablentypen werden durch die jeweils zugehörigen Werte ersetzt.
    1. Innerhalb des `<main>`-Elements wird überprüft, ob die Überschriftelemente der Ebenen `<h2>`, `<h3>`, und `<h4>` ein `id`-Attribut aufweisen. Fehlt dieses Attribut, wird basierend auf dem Text der Überschrift eine ID generiert und dem Element hinzugefügt.
    1. Wenn in einer HTML-Datei die TOC-Variable gesetzt ist, wird aus den Elementen `<h2>`, `<h3>`, und `<h4>`, die sich innerhalb des `<main>`-Elements befinden, ein Inhaltsverzeichnis der Seite erstellt. Anschließend wird die TOC-Variable durch dieses Inhaltsverzeichnis ersetzt.
    1. Sämtliche Verweise auf Grafikdateien werden aus den `src`-Attributen der `<img>`-Elemente sowie aus den `srcset`-Attributen der `<source>`-Elemente gesammelt. Dies geschieht, um später ausschließlich jene Grafikdateien zu verarbeiten und in den Zielordner zu kopieren, die tatsächlich benötigt werden.
    1. Wenn die Option `-mini` oder deren Kurzform `-m` aktiviert ist, erfolgt eine Komprimierung des HTML-Codes, indem alle Kommentare, überflüssige Leerzeichen und Zeilenumbrüche entfernt werden.
1. Die XML-Sitemaps werden auf Basis der temporären Daten generiert.
    1. Im Wurzelverzeichnis der Webseite wird standardmäßig eine Index-Sitemap-Datei angelegt. Diese verweist auf die einzelnen Sitemap-Dateien, die im Bibliotheksverzeichnis abgelegt sind. Für einsprachige Webseiten wird lediglich eine Sitemap-Datei erzeugt. Bei mehrsprachigen Webseiten hingegen wird für jede Sprachversion eine separate Sitemap-Datei angefertigt. Sobald eine Sitemap-Datei die maximale Anzahl von 50.000 Einträgen erreicht, wird automatisch eine zusätzliche Datei mit fortlaufender Nummerierung erstellt. Diese wird wiederum in der Index-Sitemap-Datei verlinkt.
1. Die SCSS-Dateien aus dem Quellverzeichnis werden in CSS-Dateien umgewandelt.
    1. Alle Teildateien werden in die Hauptdateien eingefügt.
    1. Die SCSS-Dateien im Quellverzeichnis werden in CSS-Dateien umgewandelt.
    1. Sämtliche Verweise auf Grafikdateien werden aus den `url`-Funktionen gesammelt. Dies geschieht, um später ausschließlich jene Grafikdateien zu verarbeiten und in den Zielordner zu kopieren, die tatsächlich benötigt werden.
    1. Alle in den `font-family`-Eigenschaften referenzierten Schriftarten werden erfasst, um sicherzustellen, dass lediglich die entsprechenden Schriftartdateien verarbeitet und anschließend in den Zielordner übertragen werden.
    1. Wenn die Option `-mini` oder die Kurzoption `-m` aktiviert ist, erfolgt eine Komprimierung des CSS-Codes durch Entfernen aller Kommentare, überflüssigen Leerzeichen und Zeilenumbrüche.
1. Die JavaScript-Dateien aus dem Quellverzeichnis werden verarbeitet.
    1. Alle Teildateien werden in die Hauptdateien eingefügt.
    1. Bei Verwendung der Optionen `-mini` oder der Kurzoption `-m` erfolgt eine Komprimierung des JavaScript-Codes durch das Entfernen aller Kommentare, überflüssigen Leerzeichen und Zeilenumbrüche.
1. Die Grafikdateien werden verarbeitet.
    1. Alle zuvor erfassten Grafikdateien werden jetzt in das Zielverzeichnis übertragen.
1. Die Schriftartdateien werden verarbeitet.
    1. Ist eine Schriftart im Quellverzeichnis ausschließlich im TTF-Format vorhanden, erfolgt ihre Konvertierung sowohl in das WOFF- als auch in das WOFF2-Format.
    1. Alle zuvor gesammelten Dateien werden jetzt in das Zielverzeichnis übertragen.
1. Alle weiteren Dateien werden in das Zielverzeichnis kopiert.
1. Das temporäre Verzeichnis wird wieder entfernt.

### Lokalen temporären Webserver erstellen und verwalten

Um das erstellte Ergebnis zu testen oder zu betrachten, ist ein Webserver erforderlich. Node.js ermöglicht eine schnelle und unkomplizierte Einrichtung eines solchen Servers. Aus diesem Grund ist das Live-Modul dafür konzipiert, diese Aufgabe automatisch zu erledigen.

Durch den Befehl `py wb.py live` oder der Kurzform `py wb.py l` lässt sich ein lokaler Webserver mittels Node.js im Zielverzeichnis initiieren. Falls zuvor kein Server im Zielverzeichnis eingerichtet wurde, erfolgt dessen Erstellung automatisch, woraufhin er unmittelbar gestartet wird.

#### Ablauf

- Es wird zunächst geprüft, ob eine Option aktiviert wurde.
    - Falls keine Option ausgewählt ist, erfolgt eine Überprüfung daraufhin, ob für das aktuelle Projekt bereits ein Webserver konfiguriert ist. Ist ein Webserver vorhanden, wird dieser gestartet. Andernfalls wird der Webserver zunächst eingerichtet und dann in Betrieb genommen. Nach dem Start wird stets die URL samt Port in der Kommandozeile ausgegeben.
    - Bei Verwendung der Option `-off` oder deren Kurzform `-o` wird der laufende Webserver beendet.
    - Durch Setzen der Option `-delete` oder der Kurzform `-d` wird der Webserver vollständig entfernt.

### FTP-Synchronisation

Durch den Befehl `py wb.py ftp` oder der Kurzform `py wb.py f` erfolgt eine Synchronisierung des lokalen Webseitenverzeichnisses mit dem entsprechenden Serververzeichnis. Dabei wird das Serververzeichnis stets an den aktuellen Stand des lokalen Verzeichnisses angepasst. Das bedeutet, dass Dateien und Verzeichnisse, die auf dem Server vorhanden, aber nicht mehr im lokalen Verzeichnis zu finden sind, entfernt werden. Ebenso werden auf dem Server befindliche Dateien, die älter sind als ihre lokalen Entsprechungen, aktualisiert. Nicht vorhandene Dateien und Verzeichnisse werden auf dem Server neu erstellt bzw. hinzugefügt.

Mit der Option `-clear` oder der Kurzoption `-c` wird zunächst das gesamte Serververzeichnis geleert, bevor es basierend auf dem aktuellen lokalen Verzeichnisstand neu aufgebaut wird.

## Inhalte

Idealerweise sollten die verschiedenen Frameworks einen modularen Aufbau aufweisen und gegenseitige Unterstützung bieten.

### CSS-Framework

Derzeit ist es noch unentschieden, ob ich die Entwicklung eines eigenen Frameworks in Angriff nehme oder stattdessen die Integration eines bereits bestehenden Frameworks ermögliche.

### JavaScript-Framework

Derzeit ist es noch unentschieden, ob ich die Entwicklung eines eigenen Frameworks in Angriff nehme oder stattdessen die Integration eines bereits bestehenden Frameworks ermögliche.

## Spätere Funktionen und Inhalte

- Datenbankabfragen für dynamische Inhalte: Um die Erstellung von Tabellen und Diagrammen – insbesondere dynamischer Natur – zu ermöglichen, plane ich die Integration einer Funktion, die es erlaubt, Abfragen zu generieren. Diese Abfragen sollen während des Build-Prozesses Daten extrahieren und in eine Datei einbinden. Als potenzielle Datenquellen sind CSV-, Excel/Calc- und SQLite-Dateien vorgesehen.
