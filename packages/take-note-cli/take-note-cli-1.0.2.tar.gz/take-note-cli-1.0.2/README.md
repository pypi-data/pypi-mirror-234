# Take Note
**Create and open notes in your favourite editor.**

## Features

- Written in Python with no runtime dependencies.
- Open notes files for specified week using the `code` command line for VS Code.
    - --thisWeek, --lastWeek and --nextWeek are supported.
- Organises notes in a date based folder structure from your root notes folder, e.g. 2023/08
    - set the root notes folder using --notesFolder
- Choose which editor to use with --editor
- Specify a VS Code workspace to open along with the note file with --workspace
    - This will override the --editor setting to `code`
- Specify a template file relative to the root notes folder to use when a new file is created using --template. This also performs a simple replacement of the text HEADER_DATE with the date formatted as "%A %d %B %Y" to use in the document title.

## Future features
- Support for daily notes options.
- Support for batch creation of files in advance. This is useful if you use a device where you can edit files, but can't easily create them.
- Test on older versions of Python and release for 3.8+.


## Installation

### pipx

The recommended way to install the published package is through [pipx](https://pypa.github.io/pipx/).

```
# from PyPI
pipx install take-note-cli

# direct from github
pipx install git+https://github.com/wsinned/take-note
```

## Usage

### Command Line

Specify a folder using the --notesFolder option, otherwise $HOME/Notes will be used
A week option must be supplied from --thisWeek, --lastWeek or --nextWeek

```
take-note --notesFolder=$HOME/MyNotes --thisWeek
```

A note will be created in the under the MyNotes/YYYY/mm folder named with the date of the Monday of this week, e.g. 2023-08-07-Weekly-log.md


### Aliases

Setting up aliases in you preferred shell is a great way to make accessing your notes quick and easy.

```
notes_folder="$HOME/SomePath/MyNotes"
args="--notesFolder $notes_folder --workspace notes.code-workspace --template Home-weekly-log-template.md"

alias thisWeek="take-note --thisWeek $args"
alias nextWeek="take-note --nextWeek $args"
alias lastWeek="take-note --lastWeek $args"
```

All you have to do now is type one of the following to open the desired note file.

```
> thisWeek
> lastWeek
> nextWeek
```

## Other Installation Methods

### Virtual Environment

```
python -m venv venv 

source venv/bin/activate

venv/bin/pip install -r requirements.txt

# install with tests as editable src
venv/bin/pip install -e .

```


## Development

### Nix & NixOS

The supplied shell.nix definition provides support for entering a nix-shell directly in the repository with all dependencies.

````
nix-shell --run zsh # ensure using zsh over default bash session

# only needed once, or to recreate the virtual environment
python -m venv venv 

source venv/bin/activate

# install with tests as editable src
venv/bin/pip install -e '.[test]'

# run the tests
pytest

# close the virtual environment and exit the shell when done
deactivate
exit
````


### Other Linux or MacOS

````
# only needed once, or to recreate the virtual environment
python -m venv venv 

source venv/bin/activate

venv/bin/pip install -r requirements.txt -r requirements.dev.txt

# install with tests as editable src
venv/bin/pip install -e '.[test]'

# run the tests
venv/bin/pytest

# close the virtual environment when done
deactivate
````

## Build & Publish

From an installed and tested venv, do the following:

```
# check the version:
cat src/takenote/__version__.py

# build the package
venv/bin/pyproject-build

# publish the package
venv/bin/twine upload dist/*
```
Credentials for twine should be either:
    - stored in .pypirc in the [pypi] section
    - entered at the prompt, username = __token__ and password = your_api_key

