Virtual Environment
========================================

## What is a virtual environment?
    - A isolated python environment that is installed into a directory and maintains it's own copy of python and pip (python's package manager).
    - When activated all python operations will route to the python interpreter within the virtual environment.

## What are the benefits?
    - Keeps your global site-packages directory clean and manageable.
    - Keeps system or user installed python and it's libraries untouched.
    - Solves the problem of “Project X depends on version 1.x but, Project Y needs 4.x”.
    - Development will not interfere with the System or the user's python. 
    - All libraries installed in the virtual environment will only be used within that environment.

## How to install?

    $ pip install virtualenv

## How to create a virtual environment?
In current directory:
    
    python -m venv .

In a subdirectory that does not exist:
    python -m venv ./new_dir

## How to activate a virtual environment?
##### Windows
```BatchFile
new_dir\scripts\activate.bat
```
##### OSX/Ubuntu (bash)
```Shell
. new_dir/bin/activate
```
## How to deactivate a virtual environment?
##### Windows
```BatchFile
<clone root>\env\scripts\deactivate.bat
```
##### OSX/Ubuntu (bash)
```Shell
deactivate
```