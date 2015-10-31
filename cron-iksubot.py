#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

	IKSUbot-booker

	author: Albin Hubsch - albin.hubsch@gmail.com
	copyright: 2015
	last updated: 8/9 2015

	This is the autobooker runner. It's a deamon that does all the parsing
	and automatically books from subscriptions in the databse.


'''

from Program import *
import logging
import os
import sys

PATH = os.path.abspath(os.path.split(sys.argv[0])[0])

if __name__ == '__main__':

	# Logging
	fp = PATH+'/iksubot.log'
	logging.basicConfig(filename=fp,level=logging.INFO,format='%(asctime)s.%(msecs)d | %(levelname)s | %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

	logging.getLogger("requests").setLevel(logging.WARNING)

	# Initiate program
	program = Program()

	# Catch any exceptions
	try:
		program.run()
	except Exception, e:
		logging.error(e)