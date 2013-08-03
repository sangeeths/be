#!/usr/bin/python

import smtplib

sender = 'sangeeth@riptideio.com'
receivers = ['sangeeth@riptideio.com']

message = """From: Build Engine<build@riptideio.com>
To: Sangeeth Saravanaraj<sangeeth@riptideio.com>
Subject: Build Summary for BrightEdge

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except Exception, e:
   print "Error: unable to send email; Reason [%s]" % e

