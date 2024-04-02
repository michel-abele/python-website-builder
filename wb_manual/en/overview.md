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
1. The HTML files from the source directory are processed:
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
    1. 