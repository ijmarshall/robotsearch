#!/usr/bin/env python
# -*- coding: utf-8 -*-

import robotsearch
import argparse
import os
import logging

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='RobotReviewer RCT filter: retrieves the RCTs from a database search result with state-of-the-art accuracy')
parser.add_argument('input_filename', nargs='?', help='name of RIS file to take as input')
parser.add_argument("-s", "--sensitive", action='store_true', help='Aim for high sensitivity (i.e. for systematic reviews)', required=False)
parser.add_argument("-p", "--precise", action='store_true', help='Aim for high precision (i.e. for rapid reviews/clinical question answering', required=False)
parser.add_argument("-f", "--force", action='store_true', help='Force overwrite of existing output file', required=False)
parser.add_argument("-t", "--test", action='store_true', help='Run the RobotSearch test suite', required=False)


# if not args.test and not args.input_filename:
#     print("Please enter a filename after the robotsearch command (RIS files accepted)")

args = parser.parse_args()


print("""
                   _____
                  |     |
                  | | | |
                  |_____|
                 ___|_|___

""")
print("Welcome to the RobotReviewer RCT filter :)\n\n")

if args.test:
    print("Test mode...")
    from robotsearch.robots import rct_robot
    rct_robot.test_calibration()
    quit()


if not args.input_filename:
    print("Error - No filename given. A filename for your RIS file is required, e.g. `robotsearch myrefs.ris`.")
    exit()

if not os.path.isfile(args.input_filename):
    print("Error - Sorry can't find the file '{}' - does it exist, and have you entered the path?".format(args.input_filename))
    exit()

input_file_parts = os.path.splitext(args.input_filename)

output_filename = "{}_robotreviewer_RCTs{}".format(*input_file_parts)



if os.path.isfile(output_filename):
    if not args.force:
        print("The file '{}' already exists --- have you already run RobotReviewer on this input? If you wish to run again, please rename, move or delete '{}' to something else".format(output_filename, output_filename))
        exit()
    else:
        print("The file '{}' already exist --- RobotSearch will overwrite (press Ctrl-C before prediction has completed to abort)".format(output_filename))

if args.precise and args.sensitive:
    print("Please choose either sensitive or precise search (i.e. don't run with both `-p` and `-s` arguments")
    exit()
elif args.precise:
    print("Using the precise strategy")
    filter_class = "cnn"
    threshold = "precise"

else:
    print("Using the sensitive strategy")
    filter_class = "svm"
    threshold = "sensitive"



log.info('Starting up the robots...')
from robotsearch.robots import rct_robot
rct_bot = rct_robot.RCTRobot()

log.info('Loading the RIS input file')
with open(args.input_filename, 'r') as f:
    input_text = f.read()

log.info('Finding RCTs...')
output = rct_bot.filter_articles(input_text, filter_class, threshold)

log.info('Writing the output to {}'.format(output_filename))
with open(output_filename, 'w') as f:
    f.write(output)

log.info('Finished :) Good bye!')




