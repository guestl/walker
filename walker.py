# -*- coding: utf-8 -*-

import os
import sys
import configparser
import argparse
import codecs

# First setup of pf params.
# We will resetup them later from .conf file or argparse
default_ext = '.txt'

if 'win' in sys.platform:
    default_dir = 'c:\\'
else:
    default_dir = '~'  # check for linux

out_fn = 'Computer_log_file.txt'
str_dir_list = ''
dir_list = []

# Look at command-line args
parser = argparse.ArgumentParser(description='This script scans for files in directories from default dir.',
                                 epilog='Also it can use specific .conf file.\
                                         Examples of using: \
                                         1. python walker.py -h\n \
                                         2. python walker.py -c walker2.conf -d d:\\  \
                                         3. python walker.py -e .bat,.com  \
                                         4. python walker.py -c walker2.conf -d d:\ -e .bat  \
                                         5. python walker.py -c walker2.conf -o out.txt')
parser.add_argument('--conf', '-c', type=str,
                    help='.conf file name.  \
                    If .conf file exists, then script will take exists params from the file')
parser.add_argument('--dir', '-d', type=str,
                    help='Default directory name.')
parser.add_argument('--ext', '-e', type=str,
                    help='Files extensions with leading dot. \
                          It may be a single value or comma separated list.')
parser.add_argument('--out', '-o', type=str,
                    help='Default output file name.')

args = parser.parse_args()

if args.conf:
    config_file_name = args.conf
else:
    # default config file name
    # make file from script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_name = os.path.join(script_dir, 'walker.conf')

# Trying to reach .conf file
has_config = False

if os.path.isfile(config_file_name) and os.path.getsize(config_file_name) > 0:
    print("Opening {} configuration file".format(config_file_name))
    config = configparser.ConfigParser()
    has_config = True

    try:
        config.read(config_file_name)
    except Exception as e:
        print("Error reading {} file".format(config_file_name))
        raise e


if has_config:
    if args.ext is None:
        try:
            default_ext_list = config['DEFAULT']['Extension']
        except Exception as e:
            pass
    else:
        default_ext_list = args.ext
    default_ext = default_ext_list.split(',')

    if args.dir is None:
        try:
            default_dir = config['DEFAULT']['Directory']
        except Exception as e:
            pass
    else:
        default_dir = args.dir

    if args.out is None:
        try:
            out_fn = config['DEFAULT']['Out_file_name']
        except Exception as e:
            pass
    else:
        out_fn = args.out

    try:
        str_dir_list = config['USER_SETTINGS']['DirectoryList']
        dir_list = str_dir_list.split(',')
    except Exception as e:
        pass
"""
print("config_file_name", config_file_name)
print("default_ext", default_ext)
print("default_dir", default_dir)
print("out_fn", out_fn)
print("dir_list", dir_list)
"""


def get_file_list_in_dir(dir_name):
    result_list = []
    tree = os.walk(dir_name)

    for d, dirs, files in tree:
        for file in files:
            filename, file_extension = os.path.splitext(file)
            if file_extension and file_extension in default_ext:
                path = os.path.join(d, file)
                result_list.append(path)
    return result_list


print("Scanning..")
path_f = []
if len(dir_list) > 0:
    for directory in dir_list:
        path_f.extend(get_file_list_in_dir(directory))
else:
    path_f.extend(get_file_list_in_dir(default_dir))

print("Saving results..")
try:
    file_out = codecs.open(out_fn, "w", "utf-8")
except Exception as e:
    print("Error while opening {}".format(out_fn))
    raise e

for full_f in path_f:
    full_f += "\n"
    file_out.write(full_f)

file_out.close()

print("Done")
