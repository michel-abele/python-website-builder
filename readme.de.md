[<< zurück](https://github.com/michel-abele/python-website-builder)

![GitHub Release](https://img.shields.io/github/v/release/michel-abele/python-website-builder)
![GitHub last commit](https://img.shields.io/github/last-commit/michel-abele/python-website-builder)
![GitHub repo size](https://img.shields.io/github/repo-size/michel-abele/python-website-builder)

# Python-Website-Builder
Ein CLI-Website-Builder in Python.

## Betriebssystemunterstützung

Dieses Python-Skript ist für die Betriebssysteme Windows und Linux (einschließlich Apple) konzipiert.
**Aktuell wurde das Skript nur unter Windows 11 getestet.**

## Installation

1. Installiere eine aktuelle Version von Python:
    - **Windows:** Lade dir (hier)[https://www.python.org/downloads/] die aktuelle Version von Python herunter und führe anschließend die Installationsdatei aus.
    - **Linux Desktop:** Lade dir (hier)[https://www.python.org/downloads/] die aktuelle Version von Python herunter und führe anschließend die Installationsdatei aus oder verwende den Software- bzw. Paketmanager deiner Distribution aus.
    - **Linux CLI:** Öffne ein Terminal und verwende den distributionsabhängigen Paketmanager um Python zu installieren, in der Regel heißt das Paket `python3`.
    - Fügen Sie den Systemvariablen `PATH` den Pfad zum Python-Verzeichnis und `PATHEXT` die Dateiendung `.PY` hinzu. Um das Installationsverzeichnis von Python herauszufinden, kannst du auf allen Systemen mit dem Terminal in das Benutzerverzeichnis wechseln und dort folgenden Befehl ausführen: `py -c "import sys; print(sys.executable)"`.

1. Installiere eine aktuelle Version von Git:
    - **Windows:** Lade dir (hier)[https://git-scm.com/downloads] die aktuelle Version von Git herunter und führe anschließend die Installationsdatei aus.
    - **Linux Desktop:** Lade dir (hier)[https://git-scm.com/downloads] die aktuelle Version von Git herunter und führe anschließend die Installationsdatei aus oder verwende den Software- bzw. Paketmanager deiner Distribution aus.
    - **Linux CLI:** Öffne ein Terminal und verwende den distributionsabhängigen Paketmanager um Git zu installieren, in der Regel heißt das Paket `git`.

1. Klone das Repository von GitHub:
    - Wechsel mit einem Dateimanager in das Zielverzeichnis und führe dort ein Terminal aus. In den meisten Betriebssystem mit einem Rechtsklick in den Verzeichnisbereich.
    - Klone mit folgendem Befehl das Repository in das aktuelle Verzeichnis: `git clone https://github.com/michel-abele/python-website-builder .`. Achte auf den Punkt am Ende, damit kein Unterverzeichnis mit dem Namen des Repository erstellt wird.

1. Folgende Python-Pakete müssen installiert werden:
    - Paket für die visuelle Fortschrittsanzeige: `pip install tqdm`
    - Paket für die Sass/SCSS-Kompilierung: `pip install libsass`
