[<< back](./manual.md)

# HTML

## Variables

As HTML5 does not offer any built-in functions for the use of variables, variables for the HTML processor are stored here in the form of comments. With this method, I want to prevent false-positive error messages or incorrect code highlighting in editors.

**Important:** There are currently no fixed guidelines regarding the design of variables. The replacement always takes place in a specific order: the static variables are replaced first, followed by the dynamic variables. In the event of a conflict, meaning if a variable key exists in both types, the value of the static variable is replaced.

### Static variables

Static variables are characterized by an unchangeable key and a fixed value, which they obtain from the configuration file. The assigned value remains unchanged after each build process unless it is manually adjusted before the process.

JSON file:
```json
"var_key": "var_value"
```

Variable:
```html
<p><!-- var: value --></p>
```

Replacement:
```html
<p>var_value<p>
```

### Dynamic variables

Dynamic variables are characterized by a fixed key and a variable value. This value is generated during the build process and changes with each subsequent run.

#### Modification time of the file

The variable `<!-- var: FMT -->` is replaced with the current date of the change.

#### Table of contents

The variable `<!-- var: TOC -->` is replaced with a table of contents of the current page. The table of contents contains all heading elements of the levels `<h2>`, `<h3>` and `<h4>` that are located within the `<main>` element.

## Importing part files

Partial files can be integrated using the include function. However, as HTML5 does not provide native support for such a procedure, this functionality is implemented using special comments. In order to be integrated correctly, the relevant part files must be located in the html/parts directory.

The file _./source/html/parts/global/header.html_ is included with the following specification:
```html
...
</head>

<body>

    <!-- inc: global/header -->

</body>
...
```
