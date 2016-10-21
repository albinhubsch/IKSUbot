#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

	IKSUbot-tests

'''

from Program import *
import logging
import os
import sys
import requests
import time
import datetime
from ProgramModules import *

from peewee import *
from Models import *

print 'Start Tests'

iksu = IKSU()

user = User.get(User.id == 1)

print 'hejsan' + 'dåsan'

# print iksu._signIn(user)

# print iksu.bookClass(id, user, )
