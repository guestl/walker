This script scans for files in directories from default dir.

Also it can use specific .conf files.

Examples of using:

+ `python walker.py -h`
+ *show help message*

+ `python walker.py -c walker2.conf -d d:\`
*load settings from walker2.conf. except default directory setting, it will be taken from -d param.*

+ `python walker.py -e .bat,.com`
*scan files with settings from walker.conf if exists or with default settings. except extensions list, it will be taken from -e param*

+ `python walker.py -c walker2.conf -d d:\ -e .bat`
*load settings from walker2.conf if exists or with default settings. except extensions list and default dir, it will be taken from -e and -d params*

+ `python walker.py -c walker2.conf -o out.txt`
*load settings from walker2.conf if exists or with default settings. except output file name, it will be taken from -o param*