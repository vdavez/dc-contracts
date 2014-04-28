#!/usr/bin/env python

import json
import smtplib
from datetime import date
import os

def maildata (data):
	todaydate = date.today().isoformat()

	# Initialize the Email

	fromaddr = os.environ.get('SENDTOADDR')
	toaddrs  = fromaddr
	msg = "Subject: DC Contracts Update -- " + todaydate + '\n'
	server = smtplib.SMTP("smtp.gmail.com:587")
	server.starttls()
	user = os.environ.get('GMAILUSER')
	pwd = os.environ.get('GMAILPWD')
	server.login(user,pwd)
	msg = msg + json.dumps(data, indent=2)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()

