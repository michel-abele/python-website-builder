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
1. Die HTML-Dateien aus dem Quellverzeichnis werden verarbeitet:
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
1. Alle SCSS-Dateien aus dem Quellverzeichnis werden in CSS-Dateien umgewandelt.
    1. 