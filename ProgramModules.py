#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
'''

import requests
import time
import datetime
from dateutil.parser import parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from bs4 import BeautifulSoup
import sys
import os
import logging

PATH = os.path.abspath(os.path.split(sys.argv[0])[0])

# Logging
fp = PATH+'/iksubot.log'
logging.basicConfig(filename=fp,level=logging.INFO,format='%(asctime)s.%(msecs)d | %(levelname)s | %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

logging.getLogger("requests").setLevel(logging.WARNING)

# 
class IKSU:

	# 
	def __init__(self):
		pass

	'''
		checkServerTime

		params: 
		return: True or false
	'''
	def checkServerTime(self):
		try:
			r = requests.get('https://bokning.iksu.se/')
			p = parse(r.headers['date'])

			logging.info('IKSU server time: '+str(p))

			if time.localtime().tm_isdst is 1:
				if int(p.strftime('%H')) is 22:
					return True
				else:
					return False
			else:
				if int(p.strftime('%H')) is 23:
					return True
				else:
					return False

		except Exception, e:
			logging.error(e)
			return False

	'''
		fetchClassId

		params: subscription
		return: int classId
	'''
	def fetchClassId(self, subscription):

		url = 'https://bokning.iksu.se/index.php'

		# payload = {'fromDate': '2015-09-11', 'thruDate': '2015-09-18', 'fromTime':'06:00', 'thruTime':'23:00', 'daysOfWeek[]':'2', 'locations[]':'100', 'obj_classes[g_iw]':'X', 'objects[]':'IW55', 'instructors[]':'CAHO', 'func':'fres', 'search':'T', 'btn_submit':'x'}

		now = datetime.datetime.now()
		tomorrow = now + datetime.timedelta(days=1)
		end = now + datetime.timedelta(days=8)

		payload = {'fromDate': tomorrow.strftime('%Y-%m-%d'), 'thruDate': end.strftime('%Y-%m-%d'), 'fromTime':subscription.start_tid, 'thruTime':subscription.slut_tid, 'daysOfWeek[]':subscription.dag, 'locations[]':subscription.plats, 'objects[]':subscription.traningstyp, 'instructors[]':subscription.instruktor, 'func':'fres', 'search':'T', 'btn_submit':'x'}
		
		try:
			r = requests.get(url, params=payload)

			# Extract class id
			parse = BeautifulSoup(r.content, 'html.parser')

			classId = None
			for i in parse.find_all('tr'):
				classId = i.get('id')

			return classId

		except Exception, e:
			logging.error(e)
			return False

	'''
		_signIn

		params: user
		return: session - signed in session
	'''
	def _signIn(self, user):

		# Send sign in request to IKSU
		payload = {'txt_login': user.email, 'psw_password': user.password}
		session = requests.Session()

		try:
			r = session.post("https://bokning.iksu.se/index.php?func=do_login", data=payload)

			if r.status_code is 200:
				return session
			else:
				return False
		except Exception, e:
			logging.error(e)
			return False

	'''
		confirmSignIn
		-To be implemented

		params: session
		return: True or False
	'''
	def confirmSignIn(self, session):
		pass

	'''
		bookClass
		
		params: class_id, user
		return: email adress to send confrimation email
	'''
	def bookClass(self, class_id, user, subscription):

		# Run _signIn with user params & save session cookie
		session = self._signIn(user)

		try:
			# send booking request for subscription with session cookie
			url = 'https://bokning.iksu.se/index.php?func=ar&id='+str(class_id)+'&location='+str(subscription.plats)+'&prev_f=rd'
			r = session.get(url)

			return user.email
		except Exception, e:
			logging.error(e)
			return None

	'''
		confirmBooking

		params: class_id, 
		return: True or False
	'''
	def confirmBooking(self, class_id, user, session = None):
		
		if session is None:
			session = self._signIn(user)

		r = session.get('https://bokning.iksu.se/index.php?func=mr')
		
		if soup.find(id=class_id):
			return True
		else:
			return False

# 
class Mail:

	'''
		__init__

		params: to, subscription
		return: 
	'''
	def __init__(self, to, subscription):
		self.receivers = to
		self.subscription = subscription

		with open(PATH+'/smtp.auth') as data_file:
			self.auth = json.load(data_file)


	'''
		sendConfirmationEmail

		params: 
		return: 
	'''
	def sendConfirmationEmail(self):

		days = ['MÅNDAG', 'TISDAG', 'ONSDAG', 'TORSDAG', 'FREDAG', 'LÖRDAG', 'SÖNDAG']
		
		# Define email addresses to use
		addr_to   = self.receivers
		addr_from = 'do_not_reply@iksubot.ahub.se'
		 
		# Define SMTP email server details
		smtp_server = 'smtp.iksubot.ahub.se'
		smtp_user   = self.auth['email']
		smtp_pass   = self.auth['password']
		 
		# Construct email
		msg = MIMEMultipart('alternative')
		msg['To'] = ', '.join(self.receivers)
		msg['From'] = addr_from
		msg['Subject'] = 'IKSUbot class booked, please verify!'
		 
		# Create the body of the message (a plain-text and an HTML version).
		text = "You have been automatically singed up on a class at IKSU."
		html = """\
		<html lang="en">
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
			<title>IKSUbot Confirmation</title>
			<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
		</head>
		<body style="margin: 0 0 0 0; padding: 10px 10px 10px 10px; background: #ddd;">
			<table border="0" cellpadding="0" cellspacing="0" width="100%" style="background: #fff; border-radius: 2px;">
				<tr>
					<td style="padding: 15px 15px 15px 15px;">
						<h1 style="font-family:sans-serif;">IKSUbot</h1>
						<p style="font-family:sans-serif;">We have automatically signed you up on the following class at IKSU. Please verify this by opening the IKSU app and confirm that the booking was done correctly.</p>
						<p style="font-family:sans-serif;">
							If you want to quit this subscription, contact the creator of IKSUbot.
						</p>
					</td>
				</tr>
				<tr>
					<td style="padding: 15px 15px 15px 15px;">
						<table width="100%" border="0" cellpadding="0" cellspacing="1">
							<tr>
								<td align="center" style="padding: 15px 15px 15px 15px; background: #efefef; line-height: 0;">
									<p style="font-family: sans-serif; font-size: 18px; color: #666;">"""+str(self.subscription.traningstyp)+"""</p>
								</td>
								<td align="center" style="padding: 15px 15px 15px 15px; background: #efefef; line-height: 0;">
									<p style="font-family: sans-serif; font-size: 18px; color: #666;">"""+str(self.subscription.instruktor)+"""</p>
								</td>
								<td align="center" style="padding: 15px 15px 15px 15px; background: #efefef; line-height: 0;">
									<p style="font-family: sans-serif; font-size: 18px; color: #666;">next """+days[int(self.subscription.dag)-1]+"""</p>
								</td>
								<td align="center" style="padding: 15px 15px 15px 15px; background: #efefef; line-height: 0;">
									<p style="font-family: sans-serif; font-size: 18px; color: #666;">"""+str(self.subscription.start_tid)+"""</p>
								</td>
							</tr>
						</table>
					</td>
				</tr>
				<tr>
					<td style="padding: 15px 15px 15px 15px;">
						<p style="font-family:sans-serif; text-align:center; color:#aaa;">This mail was sent to you by a robot, please do not respond to this, because she does not know how to answer.</p>
					</td>
				</tr>
			</table>
		</body>
		</html>
		"""
		 
		# Record the MIME types of both parts - text/plain and text/html.
		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(html, 'html')
		 
		# Attach parts into message container.
		# According to RFC 2046, the last part of a multipart message, in this case
		# the HTML message, is best and preferred.
		msg.attach(part1)
		msg.attach(part2)
		 
		# Send the message via an SMTP server
		s = smtplib.SMTP(smtp_server, 587)
		s.login(smtp_user,smtp_pass)

		s.sendmail(addr_from, addr_to, msg.as_string()) 
		s.quit()