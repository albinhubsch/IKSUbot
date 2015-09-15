#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

	IKSUbot

	author: Albin Hubsch - albin.hubsch@gmail.com
	copyright: 2015
	last updated: 8/9 2015

	This is the "control panel". This is the program you should use
	to handle the users, booking subscriptions etc etc.


'''

import sqlite3
import sys
import os

from peewee import *
from Models import *

# 
def mainMenu():
	print '\n\n 1. Add User\n 2. Show Users\n 3. Remove User\n 4. Add Subscription\n 5. Show Subscriptions\n 6. Edit Subscription\n 7. Remove Subscription\n 8. Add Connection'
	print '\n'

def createTables():
	User.create_table(True)
	Subscription.create_table(True)
	UserSubscription.create_table(True)


# It's the main
if __name__ == '__main__':

	createTables()

	while True:

		print '\n\n ========== IKSUbot ========== \n\n Choose an action from the menu below\n by typing the number and press enter\n Type quit to quit.'
		mainMenu()
		menuChoice = raw_input(" Please enter menu option: ")

		# Well it's the menu

		if menuChoice is '1': #Add User
		
			inp_email = raw_input(" Please enter iksu email: ")
			inp_password = raw_input(" Please enter iksu password: ")

			u = User(email=inp_email, password=inp_password)
			u.save()

		elif menuChoice is '2': #Show users
			
			print '\n -----------------------------'

			for user in User.select():
				print ' '+str(user.id)+' | '+str(user.email) + ' | ****'

		elif menuChoice is '3': #Remove user
			
			print '\n -----------------------------'

			for user in User.select():
				print ' '+str(user.id)+' | '+str(user.email)

			uid = raw_input(' Select the user you want to remove: ')

			# delete the users subscriptions
			query = UserSubscription.delete().where(UserSubscription.user == uid)
			query.execute()

			# delete user
			user = User.get(User.id == uid)
			user.delete_instance()

		elif menuChoice is '4': #Add Subscription

			inp_traningstyp = raw_input(" Please enter träningstyp: ")
			inp_instruktor = raw_input(" Please enter instruktör: ")
			inp_plats = raw_input(" Please enter plats: ")
			inp_dag = raw_input(" Please enter dag: ")
			inp_stid = raw_input(" Please enter starttid: ")
			inp_etid = raw_input(" Please enter sluttid: ")

			s = Subscription(traningstyp=inp_traningstyp, instruktor=inp_instruktor, plats=inp_plats, dag=inp_dag, start_tid=inp_stid, slut_tid=inp_etid)
			s.save()

		elif menuChoice is '5': #Show subscriptions

			print '\n -----------------------------'
			
			for sub in Subscription.select():
				print ' '+str(sub.id)+' | '+str(sub.traningstyp)+' | '+str(sub.plats)+' | '+str(sub.instruktor)+' | '+str(sub.dag)+' | '+str(sub.start_tid) + '-' + str(sub.slut_tid)

		elif menuChoice is '6': #Edit subscription
			
			print ' This function is not yet implemented'

		elif menuChoice is '7': #Remove subscription
			
			print '\n -----------------------------'
			
			for sub in Subscription.select():
				print ' '+str(sub.id)+' | '+str(sub.traningstyp)+' | '+str(sub.plats)+' | '+str(sub.instruktor)+' | '+str(sub.dag)+' | '+str(sub.start_tid) + '-' + str(sub.slut_tid)

			sid = raw_input(' Select the subscription you want to remove: ')

			# delete the users subscriptions
			query = UserSubscription.delete().where(UserSubscription.subscription == sid)
			query.execute()

			# delete subscription
			sub = Subscription.get(Subscription.id == sid)
			sub.delete_instance()

		elif menuChoice is '8': #Add Connection
			print '\n -----------------------------'
			
			for sub in Subscription.select():
				print ' '+str(sub.id)+' | '+str(sub.traningstyp)+' | '+str(sub.plats)+' | '+str(sub.instruktor)+' | '+str(sub.dag)+' | '+str(sub.start_tid) + '-' + str(sub.slut_tid)

			sid = raw_input(' Select the subscription you want to connect: ')

			for user in User.select():
				print ' '+str(user.id)+' | '+str(user.email)

			uid = raw_input(' Select the user you want to connect to this subscription: ')

			us = UserSubscription(user=int(uid), subscription=int(sid))
			us.save()

		else:
			break