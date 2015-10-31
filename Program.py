#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
'''

import sys
import requests
import time
import datetime
from ProgramModules import *
import logging
import os

from peewee import *
from Models import *

PATH = os.path.abspath(os.path.split(sys.argv[0])[0])

# 
class Program:
	
	# 
	def __init__(self):
		pass

	# 
	def run(self):

		# Logging
		fp = PATH+'/iksubot.log'
		logging.basicConfig(filename=fp,level=logging.INFO,format='%(asctime)s.%(msecs)d | %(levelname)s | %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

		logging.getLogger("requests").setLevel(logging.WARNING)

		logging.info('STARTING IKSUbot')
		
		# Create iksu object
		iksu = IKSU()
		date = datetime.datetime.today()

		# Check if any subscriptions today
		if Subscription.select().where( Subscription.dag == str(date.isoweekday())).count() is not 0:

			# Check server time, check max 5 min
			v = 0
			while iksu.checkServerTime() is False:
				
				if v is 0:
					logging.info('IKSU server time does not match, waiting 5 secs...')
				
				if v > 60:
					break
				
				time.sleep(5)
				v += 1
		
			# Loop through all subscriptions to this day
			for subscription in Subscription.select().where( Subscription.dag == str(date.isoweekday()) ):

				# Fetch upcoming class id
				classId = iksu.fetchClassId(subscription)
				if not classId:
					return False 

				# Prepare email list
				email_list = []

				# For each user, 
				for user in User.select().join(UserSubscription).join(Subscription).where(Subscription.id == subscription.id):

					# For debugging or just informational use
					logging.info('Booking class for user: ' + str(user.email))

					# Sign in and book class
					try:
						email_list.append(iksu.bookClass(classId, user, subscription))
					except Exception, e:
						logging.error('Something went wrong when trying to book class for user: '+ user.email +' - ' + str(e))
					
				# Send booking emails to all subscribers
				mail = Mail(email_list, subscription)
				mail.sendConfirmationEmail()
