[<< back](https://github.com/michel-abele/python-website-builder)

:us:

# Project overview

My goal is to provide the following content and functions by the time version 1.0 of PyWeB is released.

## Functions

### Initiating the workbench

The `py wb.py init` command or the short form `py wb.py i` cleans the current directory of existing Git repository directories and files and at the same time creates the required directories and basic files for deployment.

### Building the website

The command `py wb.py build` or the short form `py wb.py b` starts the construction of the website. During this process, partial files are integrated into the central files, variables are inserted and other pending tasks are processed.

#### Procedure

1. The required library directories are created.
1. The HTML files are synchronized from the source directory to the target directory. Empty directories and HTML files that no longer exist in the source directory are removed from the target directory. The options `-clear` and the corresponding short option `-c` pause the synchronization and lead to the deletion of all files and directories in the target directory, which results in a complete rebuild of the website.
1. The temporary directory _./temp_ will be created.
1. The HTML files from the source directory are processed.
    1. The modification times of all HTML part files are checked and temporarily saved. This allows the up-to-dateness of the main file to be determined at a later date.
    1. A check is carried out to determine whether the website is monolingual or multilingual. This information is required for the subsequent creation of the XML sitemap files.
    1. All sub-files are inserted into the main files, whereby sub-files can in turn contain further sub-files.
    1. The different variable types are replaced by the corresponding values.
    1. Within the `<main>` element, the system checks whether the heading elements of the `<h2>`, `<h3>` and `<h4>` levels have an `id` attribute. If this attribute is missing, an ID is generated based on the heading text and added to the element.
    1. If the TOC variable is set in an HTML file, a table of contents of the page is created from the elements `<h2>`, `<h3>` and `<h4>`, which are located within the `<main>` element. The TOC variable is then replaced by this table of contents.
    1. All references to graphic files are collected from the `src` attributes of the `<img>` elements and from the `srcset` attributes of the `<source>` elements. This is done so that only those graphic files that are actually required can be processed later and copied to the target folder.
    1. If the -mini option or its short form -m is activated, the HTML code is compressed by removing all comments, superfluous spaces and line breaks.
1. The XML sitemaps are generated on the basis of the temporary data.
    1. An index sitemap file is created by default in the root directory of the website. This refers to the individual sitemap files that are stored in the library directory. Only one sitemap file is created for monolingual websites. For multilingual websites, however, a separate sitemap file is created for each language version. As soon as a sitemap file reaches the maximum number of 50,000 entries, an additional file with consecutive numbering is automatically created. This in turn is linked in the index sitemap file.
1. All SCSS files from the source directory are converted into CSS files.
    1. All sub-files are inserted into the main files.
    1. The SCSS files in the source directory are converted into CSS files.
    1. All references to graphic files are collected from the `url` functions. This is done so that only those graphic files that are actually required can be processed later and copied to the target folder.
    1. All fonts referenced in the `font-family` properties are recorded to ensure that only the corresponding font files are processed and then transferred to the target folder.
    1. If the `-mini` option or the short option `-m` is activated, the CSS code is compressed by removing all comments, superfluous spaces and line breaks.
1. The JavaScript files from the source directory are processed.
    1. All sub-files are inserted into the main files.
    1. When using the `-mini` option or the short option `-m`, the JavaScript code is compressed by removing all comments, superfluous spaces and line breaks.
1. The graphic files are processed.
    1. All previously created graphic files are now transferred to the target directory.
1. The font files are processed.
    1. If a font in the source directory is only available in TTF format, it is converted to both WOFF and WOFF2 format.
    1. All previously collected files are now transferred to the target directory.
1. All other files are copied to the target directory.
1. The temporary directory is removed again.

### Create and manage local temporary web server

A web server is required to test or view the created result. Node.js enables such a server to be set up quickly and easily. For this reason, the Live module is designed to perform this task automatically.

The command `py wb.py live` or the short form `py wb.py l` can be used to initiate a local web server using Node.js in the target directory. If no server has previously been set up in the target directory, it will be created automatically and started immediately.

#### Procedure

- The system first checks whether an option has been activated.
    - If no option is selected, a check is made to see whether a web server is already configured for the current project. If a web server is available, it is started. Otherwise, the web server is first set up and then put into operation. After starting, the URL and port are always displayed in the command line.
    - If the `-off` option or its short form `-o` is used, the running web server is terminated.
    - By setting the `-delete` option or the short form `-d`, the web server is completely removed.

### FTP synchronization

The command `py wb.py ftp` or the short form `py wb.py f` is used to synchronize the local website directory with the corresponding server directory. The server directory is always adapted to the current status of the local directory. This means that files and directories that exist on the server but can no longer be found in the local directory are removed. Files on the server that are older than their local counterparts are also updated. Files and directories that do not exist are newly created or added on the server.

With the `-clear` option or the short option `-c`, the entire server directory is first emptied before it is rebuilt based on the current local directory status.

## Contents

Ideally, the various frameworks should have a modular structure and offer mutual support.

### CSS-Framework

At the moment, it is still undecided whether I will tackle the development of my own framework or instead enable the integration of an existing framework.

### JavaScript-Framework

At the moment, it is still undecided whether I will tackle the development of my own framework or instead enable the integration of an existing framework.

## Later functions and content

- Database queries for dynamic content: To enable the creation of tables and diagrams - especially of a dynamic nature - I plan to integrate a function that allows queries to be generated. These queries should extract data during the build process and integrate it into a file. Potential data sources are CSV, Excel/Calc and SQLite files.
