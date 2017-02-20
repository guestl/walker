This script scans for files in directories from default dir.

Also it can use specific .conf files.

Examples of using:

0. `python walker.py -h`
>*show help message*

1. `python walker.py -c walker2.conf -d d:\`
>*load settings from walker2.conf. except default directory setting, it will be taken from -d param.*

2. `python walker.py -e .bat,.com`
>*scan files with settings from walker.conf if exists or with default settings. except extensions list, it will be taken from -e param*

3. `python walker.py -c walker2.conf -d d:\ -e .bat`
>*load settings from walker2.conf if exists or with default settings. except extensions list and default dir, it will be taken from -e and -d params*

4. `python walker.py -c walker2.conf -o out.txt`
>*load settings from walker2.conf if exists or with default settings. except output file name, it will be taken from -o param*