[<< back](./manual.md)

# Installation

1. Install a current version of Python:
    - **Windows:** Download the latest version of Python [here](https://www.python.org/downloads/) and then run the installation file.
    - **Linux Desktop:** Download the latest version of Python [here](https://www.python.org/downloads/) and then execute the installation file or use the software or package manager of your distribution.
    - **Linux CLI:** Open a terminal and use the distribution dependent package manager to install Python, usually the package is called `python3`.
    - Add the path to the Python directory to the system variables `PATH` and the file extension `.PY` to `PATHEXT`. To find out the Python installation directory, you can change to the user directory with the terminal on all systems and execute the following command there: `py -c "import sys; print(sys.executable)"`.

1. Install a current version of Git:
    - **Windows:** Download the latest version of Git [here](https://git-scm.com/downloads) and then run the installation file.
    - **Linux Desktop:** Download the latest version of Git [here](https://git-scm.com/downloads) and then execute the installation file or use the software or package manager of your distribution.
    - **Linux CLI:** Open a terminal and use the distribution dependent package manager to install Git, usually the package is called `git`.

1. Clone the repository from GitHub:
    - Use a file manager to change to the target directory and run a terminal there. In most operating systems, right-click in the directory area.
    - Clone the repository into the current directory with the following command: `git clone https://github.com/michel-abele/python-website-builder .`. Pay attention to the dot at the end so that no subdirectory with the name of the repository is created.

1. The following Python packages must be installed:
    - Package for visual progress display: `pip install tqdm`
    - Package for Sass/SCSS compilation: `pip install libsass`
