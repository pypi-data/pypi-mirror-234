# TSL

TSL - The State Library Module

## Maintenance

Developed and maintained by [TurtleTraction](www.turtletraction.com).

## Overview

**T**he **S**tate **L**ibrary aims to provide a way to document state files in a consistant manner, similar to `sys.doc`.

By adding the `DOC` section below to the top of the states file the following feature are enabled.

* State file overview
* Searchable state file estate
* Automated Variable extraction
  * Pillar
  * Grains
  * Include

```
#START-DOC
# File_name: state.sls
# Author: XXXXXX
# Description:
# Grains (if applicable):
# Pillars (if applicable):
# Syntax: XXXXXX
#END-DOC
```


## Quickstart

To get started with TSL:

### Install the extention on the minion

For Salt onedir package (3006 and up):

`sudo salt '<minion>' pip.install saltext.tsl`

or

`sudo salt-pip install saltext.tsl`

For classic Salt package (pre 3006):

`sudo pip install saltext.tsl`

### Test (Listing states for a specific minion included in highstate)

`sudo salt '<minion>' tsl.list`

### Use sys.doc to list all tsl functions

`sudo salt '<minion>' sys.doc tsl`

For any queries please send an email to info@turtletraction.com

## Doc header generator

TSL contains an additional standalone script that is not installed with the extension: [tsl-add-header.py](https://gitlab.com/turtletraction-oss/saltext-tsl/-/blob/main/src/tsl-add-header.py?ref_type=heads). You can use it to automatically add the doc header to any number of `sls` files:

```
python tsl-add-header.py path/to/sls-file-or-directory
```

For usage details, run the following command:

```
python tsl-add-header.py --help
```

## Development

To get started with your new project:

    # Create a new venv
    python3 -m venv env --prompt saltext-tsl
    source env/bin/activate

    # On mac, you may need to upgrade pip
    python -m pip install --upgrade pip

    # On WSL or some flavors of linux you may need to install the `enchant`
    # library in order to build the docs
    sudo apt-get install -y enchant

    # Install extension + test/dev/doc dependencies into your environment
    python -m pip install -e '.[tests,dev,docs]'

    # Run tests!
    python -m nox -e tests-3

    # skip requirements install for next time
    export SKIP_REQUIREMENTS_INSTALL=1

    # Build the docs, serve, and view in your web browser:
    python -m nox -e docs && (cd docs/_build/html; python -m webbrowser localhost:8000; python -m http.server; cd -)

    # Run the example function
    salt-call --local tsl.hello
