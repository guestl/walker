# User manual

## Intro
This script scans for files in directories from default dir.

There are many ways of setting up the script. It can be default settings, settings from .conf files, command-line arguments, and, finally, settings from internal menu. As output the script generates txt files with date time in the filename.

Default scipt settings have a lowest priority
Next priority have the settings from internal menu
Next have settings from the conf file
The highest priority have settings from command-line args

## Internal menu
Internal menu is available if user run script without any additional params.

Internal menu has choices:

0. Use only script default directory
 >*In this case script will run  with default params which are written in source code in "def_parms" dictionary. Directory for scan C: or ~, filename extension .txt as search criteria, output filename Computer_log_file + datetime.txt*
 
1. Use manually entered custom folder
 >*In this case script will run  with default params which are written in source code in "def_parms" dictionary. but folder will be entered manually.
 
2. Use folder list from manually entered filename
 >*In this case script will run  with default params which are written in source code in "def_parms" dictionary. but directories list will be loaded from file what filename you will enter.*

3. Use manually entered custom conf file
 >*In this case custom conf file will be loadeda and its settings will be used*
 
4. Exit from the script
 >*Just close the script and exit to OS*

## Examples of using

0. `python walker.py`
>*The script will show a internal menu with choices.*

1. `python walker.py -h`
>*show help message for command line args*

2. `python walker.py -c findpictures.conf -d d:\`
>*load settings from walker2.conf. except directory setting, this setting will be taken from -d param.*

3. `python walker.py -e .bat,.com`
>*scan files with default settings. except extensions list, it will be taken from -e param*

4. `python walker.py -c walker.conf -d d:\ -e .bat`
>*load settings from homedir.conf if exists or with default settings. except extensions list and default dir, it will be taken from -e and -d params*

5. `python walker.py -dlf dirlist.txt -o out.txt`
>*Script will use default settings. Except output file name, it will be taken from -o param and except directory list. The list will be loaded from -dlf param*

## Conf file structure

Good use case for conf file is spesific conf file for every use case. For example, one conf file for search pictures, second conf file for search executable files etc. User can load settings from conf files with command-line arguments or via internal script menu.

*Remarks: sumbol ";" is a start comment string symbol in a conf file. Also conf file can have a empty param* 
*If there is a commented line or empy param, the script will use settings from command-line if exist or from default script params. If exists commented parameter the sript will use its own default settings.*

[USER_SETTINGS]

Extension = .bat,.exe

> Comma separated extensions lists. Here you can write list of file extensions or a single extension. If empty or commented the script will use its own default settings

Out_file_name = Computer_log_file.txt

> Out file name. If empty or commented the script will use its own default settings

FileWithDirectoryList = ''

> Script will read directory list from file with this filename.  If empty or commented the script will use its own default settings

DirectoryListForScan = d:\\Boris\\Documents\\,d:\\tools\\,d:\\games\\

> Comma separated directory list for scanning. If empty or commented the script will use its own default settings
