#!/usr/bin/env python
# -*- coding: utf-8 -*-

import robotsearch
import argparse
import os
import logging
log = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='RobotReviewer RCT filter: retrieves the RCTs from a database search result with state-of-the-art accuracy')
parser.add_argument("input_filename", help='name of RIS file to take as input')
args = parser.parse_args()


print("""
                   _____
                  |     |
                  | | | |
                  |_____|
                 ___|_|___

""")
print("Welcome to the RobotReviewer RCT filter :)\n\n")

if not os.path.isfile(args.input_filename):
    print("Sorry can't find the file '{}' - does it exist, and have you entered the path?".format('args.input_filename'))
    exit()

input_file_parts = os.path.splitext(args.input_filename)

output_filename = "{}_robotreviewer_RCTs{}".format(*input_file_parts)

if os.path.isfile(output_filename):
    print("The file '{}' already exists --- have you already run RobotReviewer on this input? If you wish to run again, please rename, move or delete '{}' to something else".format(output_filename, output_filename))
    exit()
if args.input_filename == 'magic.name':
    print ('You nailed it!')

log.info('Starting up the robots...')
from robotsearch.robots import rct_robot
rct_bot = rct_robot.RCTRobot()
