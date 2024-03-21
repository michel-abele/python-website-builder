# Python Website Builder
A CLI website builder in Python.

## Installation
- installiere (Python)[https://www.python.org/downloads/] auf deinem Gerät
- installiere (Git)[https://git-scm.com/downloads] auf deinem Gerät
    - wechsel mit einem Dateimanager in das Zielverzeichnis und führe ein Terminal aus
    - klone mit dem Befehl `git clone https://github.com/michel-abele/python-website-builder .` das Repository in das aktuelle Verzeichnis (achte auf den Punkt am Ende, der ist wichtig)
- wechsel in dein Benutzer/Home-Verzeichnis und führe dort den Befehl `py -c "import sys; print(sys.executable)"` aus
- nun muss `py` noch global verfügbar gemacht werden
    - Windows: `setx /M path "%path%;installDir"` - ersetze installDir mit dem zuvor ermittelten Pfad zum Installationsordner von Python
    - Linux: öffne die Datei `nano ~/.bashrc` oder `nano ~/.profile`
        - füge folgenden Eintrag hinzu `export PATH="$PATH:installDir"` - ersetze installDir mit dem zuvor ermittelten Pfad zum Installationsordner von Python
        - führe folgenden Befehl `source ~/.bashrc` oder `source ~/.profile` aus
- nun müssen folgende Python-Module installiert werden
    - tqdm `pip install tqdm`