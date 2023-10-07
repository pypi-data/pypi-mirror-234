<h1 align="center">pyjetbrains</h1>

<p align="center"><i>Take the control over JetBrains IDEs Family with python code!</i></p>

---

<h2 align="center">Installation</h2>

Pyjetbrains can be installed via [Python Package Index (PyPi)](https://pypi.org/project/pyjetbrains/)
command:

```shell
pip install pyjetbrains
```

---

<h2 align="center">Features</h2>

- Open IDE projects (whole folder)
- Open files for editing
- Open file at specific character and line
- Compare multiple files
- Format files
- Currently supports Windows only, **Linux and Mac comming soon**!

It also tries to search for installed path on it's own, so you don't have to specify
location of any of installed IDE inside pyjetbrains.

**For Toolbox Users:** Toolbox installs with CLI path automatically so it's much
easier to find jetbrains IDE with toolbox.

---

<h2 align="center">Documentation</h2>

All `pyjetbrains` have required parameter of IDE as value of Enum.

**All methods have their documentation visible while using IDE!**

### Checking if IDE is Installed

Before using any of pyjetbrains method, pyjetbrains automatically checks whether
is desired IDE installed or not, but you can check it manually.

```python
import pyjetbrains

pyjetbrains.is_installed(pyjetbrains.IDE.PYCHARM)
```

### Opening files and folders

For opening files or folders _(as project)_ there is `subprocess.open()` method.

```python
import pyjetbrains

pyjetbrains.open(
    pyjetbrains.IDE.INTELLIJ_IDEA,  # IDE
    "hello_world.txt",              # Path
    line=5,                         # Line caret cursor position
    column=7                        # Column caret cursor position
)

pyjetbrains.open(
    pyjetbrains.IDE.CLION,                  # IDE
    "main.cpp", "hero.cpp", "vilain.cpp"    # Multiple Paths
)

my_paths = ["main.cpp", "hero.cpp", "vilain.cpp"]

pyjetbrains.open(
    pyjetbrains.IDE.PHPSTORM,   # IDE
    my_paths                    # Multiple paths passed as list
)

pyjetbrains.open(
    pyjetbrains.IDE.RUBYMINE,   # IDE
    "my_awesome_project"        # Folder which will open as project
)
```

### Comparing files (2 up to 3 files)

Comparing files is done with `pyjetbrains.compare_files()` method, that takes
from two to three files. After execution, difference tab of provided paths is opened.

```python
import pyjetbrains

pyjetbrains.compare_files(
    pyjetbrains.IDE.PYCHARM,    # IDE
    "project1/main.py",         # First path
    "project2/main.py",         # Second path
    "project3/main.py"          # Third path
)
```

### Formating files

For formatting files you cannot have already opened instance of desired IDE, because
Jetbrains assumes that you can use format command in IDE rather than do it with CLI.

Then you specify files or folders with code to format it with and whether it 
should be recursive.

About mask, here is cite from jetbrains site:

> Specify a comma-separated list of file masks that define the files 
> to be processed. You can use the * (any string) and ? (any single character) 
> wildcards.

```python
import pyjetbrains

pyjetbrains.format_files(
    pyjetbrains.IDE.PYCHARM, # IDE
    "my_python_project",     # Paths to format (project folder in this case)
    mask="file??.py",        # File mask
    recursive=True           # Processing directories recursively
)
```