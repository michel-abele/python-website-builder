[<< zurück](./handbuch.md)

# HTML

## Variablen

Da HTML5 keine eingebauten Funktionen für die Verwendung von Variablen bietet, werden hier Variablen für den HTML-Prozessor in Form von Kommentaren hinterlegt. Durch diese Methode möchte ich verhindern, dass es in Editoren zu falsch-positiven Fehlermeldungen oder inkorrekten Code-Hervorhebungen kommt.

**Wichtig:** Derzeit existieren keine festgelegten Richtlinien bezüglich der Gestaltung von Variablen. Die Ersetzung erfolgt stets in einer spezifischen Reihenfolge: Zuerst werden die statischen Variablen ersetzt, gefolgt von den dynamischen Variablen. Bei einem Konflikt, also wenn ein Variablenschlüssel in beiden Typen vorhanden ist, wird der Wert der statischen Variable ersetzt.

### Statische Variablen

Statische Variablen zeichnen sich durch einen unveränderlichen Schlüssel sowie einen festgelegten Wert aus, den sie aus der Konfigurationsdatei beziehen. Der zugewiesene Wert bleibt nach jedem Build-Prozess unverändert, es sei denn, er wird vor dem Prozess manuell angepasst.

JSON-Datei:
```json
"var_key": "var_value"
```

Variable:
```html
<p><!-- var: var_key --></p>
```

Ersatz:
```html
<p>var_value<p>
```

### Dynamische Variablen

Dynamische Variablen zeichnen sich durch einen festen Schlüssel und einen variablen Wert aus. Dieser Wert wird im Verlauf des Build-Prozesses generiert und verändert sich bei jedem darauffolgenden Durchlauf.

#### Änderungszeit der Datei

Die Variable `<!-- var: FMT -->` wird mit dem aktuellem Datum und der Zeit der Änderung ersetzt.

#### Inhaltsverzeichnis

Die Variable `<!-- var: TOC -->` wird mit einem Inhaltsverzeichnis der aktuellen Seite ersetzt. Das Inhaltsverzeichnis enthält alle Überschriftenelemente der Ebenen `<h2>`, `<h3>` und `<h4>` die sich innerhalb des `<main>`-Elements befinden.

## Teildateien importieren

Teildateien lassen sich mittels der include-Funktion integrieren. Da HTML5 jedoch keine native Unterstützung für ein solches Vorgehen bietet, wird diese Funktionalität durch spezielle Kommentare umgesetzt. Um korrekt eingebunden zu werden, müssen sich die betreffenden Teildateien im Verzeichnis html/parts befinden.

Die Datei _./source/html/parts/global/header.html_ wird mit folgender Angabe eingebunden:
```html
...
</head>

<body>

    <!-- inc: global/header -->

</body>
...
```
