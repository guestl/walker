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

conf file structure:

[DEFAULT]

Directory = D:\\Boris\\Documents\\Projects\\

> Start directory

; comma separated extensions lists
Extension = .bat,.pyc

> Here you can write list of file extensions

Out_file_name = Computer_log_file.txt

> Out file name

[USER_SETTINGS]

; may be empty. if not - script will read directory list from file with this filename
FileWithDirectoryList = ''

> This feature wasn't developed

; comma separated directories list
DirectoryList = d:\\Boris\\Documents\\,d:\\tools\\,d:\\games\\

> Directory list for scanning