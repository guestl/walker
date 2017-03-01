# -*- coding: utf-8 -*-

"""
1. If you run script without any command-line params,
    the script wil show some kind of menu with 3 choices:
    1. default folder (c: or ~, for instance)
    2. custom folder (user have to input the folder name)
    3. folder list (from .conf file is exists or do nothing)

2. Add date and time in output filename

3. If you run script with .conf file name or with others command-line params
    the script will use these params for scanning. Command line params have
    highest priority than .conf file params or script params

"""
import os
import sys
import configparser
import argparse
import codecs
import logging
import datetime


# *********************************************
def get_menu_choice():
    def print_menu():
        print(30 * "-", "WALKER MENU", 30 * "-")
        print("1. Use only script default directory ")
        print("2. Use manually entered custom folder ")
        print("3. Use folder list from manually entered filename ")
        print("4. Use manually entered custom conf file ")
        print("5. Use manually entered conf files directory ")
        print("6. Exit from the script ")
        print(73 * "-")

    loop = True
    int_choice = -1

    while loop:          # While loop which will keep going until loop = False
        print_menu()    # Displays menu
        choice = input("Enter your choice [1-6]: ")

        if choice == '1':
            int_choice = 1
            loop = False
        elif choice == '2':
            choice = ''
            while len(choice) == 0:
                choice = input("Enter custom folder name(s). \
It may be a list of folder's names (example: c:,d:\docs): ")
            int_choice = 2
            loop = False
        elif choice == '3':
            choice = ''
            while len(choice) == 0:
                choice = input("Enter a single filename of a file \
with custom folders list: ")
            int_choice = 3
            loop = False
        elif choice == '4':
            choice = ''
            while len(choice) == 0:
                choice = input("Enter a single filename of a file \
with custom folders list: ")
            int_choice = 4
            loop = False
        elif choice == '5':
            choice = ''
            while len(choice) == 0:
                choice = input("Enter a name of a directory \
with conf files: ")
            int_choice = 5
            loop = False
        elif choice == '6':
            print("Exiting..")
            sys.exit()
        else:
            # Any inputs other than values in if statements we print an error message
            input("Wrong menu selection. Enter any key to try again..")
    return [int_choice, choice]


# *********************************************
def get_processed_menu_choice(menu_choice, default_parms):
    if menu_choice[0] == 1:
        return default_parms
    if menu_choice[0] == 2:
        default_parms['dir_list'] = menu_choice[1].split(',')
    if menu_choice[0] == 3:
        default_parms['cdl_fn'] = menu_choice[1]
    if menu_choice[0] == 4:
        default_parms['conf_fn'] = menu_choice[1]
    if menu_choice[0] == 5:
        default_parms['conf_dir'] = menu_choice[1]
    return default_parms


# *********************************************
def show_wait(text, i):
    if (i % 4) == 0:
        print(text + '%s' % ("/"), end='\r')
    elif (i % 4) == 1:
        print(text + '%s' % ("-"), end='\r')
    elif (i % 4) == 2:
        print(text + '%s' % ("\\"), end='\r')
    elif (i % 4) == 3:
        print(text + '%s' % ("|"), end='\r')
    elif i == -1:
        print(text + 'Done!')
        print()


# *********************************************
def get_file_list_in_dir(dir_name, ext_list):
    result_list = []

    tree = os.walk(dir_name)
    i = 0

    logging.debug('get_file_list_in_dir(). dir_name is %s' % (dir_name))

    for d, dirs, files in tree:
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension and file_extension in ext_list:
                path = os.path.join(d, file)
                path = os.path.abspath(path)
                result_list.append(path)
                show_wait("Scaning    ", i)
                i += 1
    show_wait("Scaning    ", -1)

    return result_list


# *********************************************
def load_custom_directories_list_from_file(cdl_filename):
    if os.path.isfile(cdl_filename):
        try:
            with codecs.open(cdl_filename, 'r', 'utf-8') as f:
                cdl_file_content = f.readlines()
                # remove special chars like `\n` at the end of each line
                cdl_file_content = [x.strip() for x in cdl_file_content]

                return cdl_file_content
        except Exception as e:
            logging.error(e)
            raise e
    return []


# *********************************************
def get_parms_from_conf_file(conf_file_name, default_parms):
    ret_params = default_parms.copy()
    config = configparser.ConfigParser()

    try:
        logging.debug("Opening %s file" % conf_file_name)
        config.read(conf_file_name)
    except Exception as e:
        print("Error reading {} file".format(conf_file_name))
        logging.error("Error reading %s file" % conf_file_name)
        raise e

    try:
        ret_params['ext'] = config['USER_SETTINGS']['Extensions'].split(',')
    except Exception as e:
        logging.error("Error reading ['USER_SETTINGS']['Extensions'] in %s file" % conf_file_name)
        pass

    try:
        ret_params['out_fn'] = config['USER_SETTINGS']['Out_file_name']
    except Exception as e:
        logging.error("Error reading ['USER_SETTINGS']['Out_file_name'] in %s file" % conf_file_name)
        pass

    try:
        ret_params['cdl_fn'] = config['USER_SETTINGS']['FileWithDirectoryList']
    except Exception as e:
        logging.error("Error reading ['USER_SETTINGS']['FileWithDirectoryList'] in %s file" % conf_file_name)
        pass

    try:
        ret_params['dir_list'] = config['USER_SETTINGS']['DirectoryListForScan'].split(',')
    except Exception as e:
        logging.error("Error reading ['USER_SETTINGS']['DirectoryListForScan'] in %s file" % conf_file_name)
        pass

    return ret_params


logging.basicConfig(filename='walker.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(lineno)d - %(message)s')

logging.debug('#' * 50)
logging.debug('----   ---   start processing params   ----   ---')

# First setup of script params.
# We will resetup them later from .conf file, argparse or user input

logging.debug('sys.platform is %s' % sys.platform)

# default script directory for scanning
if 'win' in sys.platform:
    default_app_dir_for_scan = 'c:\\'
else:
    default_app_dir_for_scan = '/home'  # check for linux

version = '3.5'
# default script params
def_parms = dict(ext=['.txt'],
                 cdl_fn=None,
                 dir_list=[default_app_dir_for_scan],
                 out_fn='Computer_log_file.txt',
                 conf_fn=None,
                 conf_dir=None)

str_dir_list = ''

# we will use these params as scan params
walker_parms = dict(ext=[],
                    cdl_fn=None,
                    dir_list=def_parms['dir_list'],
                    out_fn=def_parms['out_fn'],
                    conf_fn=None,
                    conf_dir=None)

walker_parms_list = []
menu_choice = []

# getting script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
logging.debug('script directory is %s' % script_dir)

print('Directories scanner. Version %s' % version)
logging.debug('Script version is %s' % version)

# Look at command-line args
parser = argparse.ArgumentParser(description='This script scans for files in directories from default dir.')
parser.add_argument('--conf', '-c', type=str,
                    help='.conf file name.  \
                    If .conf file exists, then script will take \
                    exists params from the file \
                    excepts additional params in command line.')
parser.add_argument('--dl', '-dl', type=str,
                    help='Comma separated directory list for scaning.')
parser.add_argument('--dlf', '-dlf', type=str,
                    help='Filename of file with directory list for scaning.')
parser.add_argument('--cdir', '-cdir', type=str,
                    help='Directory with conf files.')
parser.add_argument('--ext', '-e', type=str,
                    help='Files extensions with leading dot. \
                          It may be a single value (.txt) or \
                          comma separated list (.txt,.log).')
parser.add_argument('--out', '-o', type=str,
                    help='Output file name. \
                    Default value is "Computer_log_file"')

args = parser.parse_args()
logging.debug('args is %s' % args)

# ****************************************
"""
if no args:
    params.dirlist = show_menu
elif have conf:
    params = data from conf
elif have conf and args:
    params = data from conf
    params = args
"""
# ****************************************

if not len(sys.argv) > 1:
    # There are no command-line args
    menu_choice = get_menu_choice()

    walker_parms = get_processed_menu_choice(menu_choice, def_parms)

    logging.debug('There are no command-line args and we are in show_menu')
    logging.debug('Menu choice is %s' % menu_choice)
    logging.debug("walker params are %s after menu processing" % walker_parms)
else:
    logging.debug('There are existing command-line args \
and we are going to process these args')

    logging.debug("Args.conf is %s" % args.conf)
    if args.conf and os.path.isfile(args.conf) and os.path.getsize(args.conf) > 0:
        # Trying to reach .conf file
        print("Opening {} configuration file".format(args.conf))
        logging.debug("Opening %s configuration file" % args.conf)

        walker_parms = get_parms_from_conf_file(args.conf, def_parms)
        logging.debug("walker params are %s after configuration file processing" % walker_parms)

    if args.ext:
        walker_parms['ext'] = args.ext.split(',')

    if args.dl:
        walker_parms['dir_list'] = args.dl.split(',')

    if args.cdir:
        walker_parms['conf_dir'] = args.cdir

    if args.out:
        walker_parms['out_fn'] = args.out

    if args.dlf:
        walker_parms['cdl_fn'] = args.dlf
    logging.debug("walker params are %s after command line args processing" % walker_parms)

if walker_parms['conf_fn']:
    if os.path.isfile(walker_parms['conf_fn']) and os.path.getsize(walker_parms['conf_fn']) > 0:
        print("Opening {} configuration file".format(walker_parms['conf_fn']))
        logging.debug("Opening %s configuration file" % walker_parms['conf_fn'])

        walker_parms = get_parms_from_conf_file(walker_parms['conf_fn'], def_parms)
        logging.debug("walker params are %s after configuration file processing" % walker_parms)
    else:
        logging.error("Error while opening %s configuration file" % walker_parms['conf_fn'])
        print('Unable to open %s file' % walker_parms['conf_fn'])

# adding custom directory list from file
if walker_parms['cdl_fn']:
    cdl_list = load_custom_directories_list_from_file(walker_parms['cdl_fn'])
    if len(cdl_list) is not None:
        walker_parms['dir_list'] = cdl_list
    logging.debug("walker params are %s after custom dir list processing" % walker_parms)

# processing conf directories list
if walker_parms['conf_dir']:
    logging.debug("we have a conf files directory as a param")
    conf_files_list = []
    if os.path.isdir(walker_parms['conf_dir']):
        print("Reading a conf files directory..")
        logging.debug("Directory %s is exists" % walker_parms['conf_dir'])
        conf_files_list = get_file_list_in_dir(walker_parms['conf_dir'], ['.conf'])
    if len(conf_files_list) < 1:
        print("There is a conf directory param. but no conf files in directory %s" % walker_parms['conf_dir'])
        print("Exiting")
        sys.exit()

    for one_conf in conf_files_list:
        if os.path.isfile(one_conf) and os.path.getsize(one_conf) > 0:
            print("Try to open {} configuration file".format(one_conf))
            logging.debug("Try to open %s configuration file" % one_conf)

            single_params_list = get_parms_from_conf_file(one_conf, def_parms)
            logging.debug("Adding %s into walker params list" % single_params_list)
            walker_parms_list.append(single_params_list.copy())
            logging.debug("walker params list is %s after %s configuration file processing" % (walker_parms_list, one_conf))
        else:
            logging.error("Error while opening %s configuration file" % one_conf)
            print('Unable to open %s file' % one_conf)
else:
    walker_parms_list.append(walker_parms)

logging.debug('----   ---   start working   ----   ---')

for single_param in walker_parms_list:
    logging.debug('----   ---   iteration   ----   ---')
    scan_result_list = []
    logging.debug('params for the iteration are %s' % single_param)

    if len(single_param['dir_list']) == 0:
        print("Nothing to scan")
        sys.exit()

    for directory in single_param['dir_list']:
        if os.path.isdir(directory):
            logging.debug('We are using %s as root directory' % directory)
            scan_result_list.extend(get_file_list_in_dir(directory, single_param['ext']))
        else:
            logging.debug('Directory %s does not exists. Skipped' % directory)
            print('Directory %s does not exists. Skipped' % directory)

    print("Saving results..")
    try:
        out_name, f_ext = os.path.splitext(single_param['out_fn'])
        single_param['out_fn'] = ''.join([out_name, "__", datetime.datetime.now().strftime("%m-%d-%Y_%I_%M_%S,%f_%p"), f_ext])
        logging.debug("single_param['out_fn'] with datetime suffix is %s" % single_param['out_fn'])
        with codecs.open(single_param['out_fn'], "w", "utf-8") as file_out:
            for full_fn in scan_result_list:
                full_fn += "\n"
                file_out.write(full_fn)

    except Exception as e:
        print("Error while opening {}".format(single_param['out_fn']))
        raise e

print("Done")
