#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
import os
import sys

PATH = os.path.abspath(os.path.split(sys.argv[0])[0])

class BaseModel(Model):
	class Meta:
		database = SqliteDatabase(PATH+'/iksubot_db.sqlite')

'''
The Users Model
'''
class User(BaseModel):
	email = CharField()
	password = CharField()

'''
The Subscriptions Model
'''
class Subscription(BaseModel):
	traningstyp = CharField()
	instruktor = CharField()
	plats = CharField()
	dag = CharField()
	start_tid = CharField()
	slut_tid = CharField()

'''
RelationModel between users and subscriptions
'''
class UserSubscription(BaseModel):
	user = ForeignKeyField(User)
	subscription = ForeignKeyField(Subscription)
