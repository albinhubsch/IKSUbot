#IKSUbot
The IKSUbot is a robot that automates class booking at the IKSU training center. It can be really hard to get a spot at popular classes like Indoor Walking or Total Training. This robot solves this by automatically sign you in and book the desired class as soon as they are released and open for booking. It can't guarantee a place but the probability of every spot being taken at the exact moment of release is very low.

The bot can in theory handle unlimited number of users and class subscriptions but the more you have the longer time you need and other bot might steal seats. The IKSU server is quite slow, expect around 3-5 seconds per user and class booking.

##How it works
The bot is very simple. It consists of two main parts. One cron worker that runs every midnight. This cron worker uses the IKSU web interface to sign in the users and book them at classes. The other part is the admin interface. This is where you can add users to the bot and add classes that the users want to subscribe to.

##How to use
First, you need a computer that can be running 24h 7days a week. A raspberry pi is perfect for this kind of work. The program is written in python 2.7 and you need to install the following additional python packages.

 - peewee
 - sqlite3
 - requests
 - BeautifulSoup
 - python-dateutil

These packages might need other additional packages depending on you system. In case just do a test run of the programs and python will tell you what is missing.

The iksubot requires you to install a crontab for the bot in order to work. It is the cron-iksubot.py file that should be linked in your crontab. Set the crontab to run every midnight. You can reach your crontab by typing

```
	sudo crontab -e
```
	
In the crontab, add this line at the end of the file. Write out and exit.

```
	#IKSUbot RUN EVERY MIDNIGHT
	0 0 * * * /usr/bin/python dir-to-directory/cron-iksubot.py
```

To add a user and a subscription to the bot run the IKSUbot.py. When adding a new user type in email and password in clear text. To add a subscription you have to follow some conventions.

 - träningstyp : The training type id (e.g "IW55") can be found by inspecting the IKSU website
 - instruktör : The instructor system id (e.g "MIJO") can be found by inspecting the IKSU website
 - plats : The place id (e.g "100" for iksu sport) can be found by inspecting the IKSU website
 - dag : The day in number 1-7 (e.g "2" for tuesday)
 - starttid: A time with ":" (e.g "18:00")
 - sluttid: A time with ":" (e.g "18:00")

You can find all data by investigating the iksu booking website URL or html source. Just search for the class and watch the url.

##Sources

 - [IKSU bokning](http://bokning.iksu.se)

##Contribute
Please feel free to contribute to this project. Just make sure you try to follow the coding conventions.

##To Do
This program is in a very early beta. It does work in current state but it might be a bit unstable an maybe crash sometimes. I'll do my best to continue the development of this. If you want to contribute please read the contribute section.

Things to do

 - Add an installer (some files is not included in the git repo due to sensitive data. These files should be created on install)
 - Create a better user flow and menu system in the Admin interface
 - Add the ability to delete connections between subscriptions and users.
 - A better mail system
 - Kill bugs