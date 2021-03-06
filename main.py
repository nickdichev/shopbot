import shopbot
import notify
import argparse
import config
import sys
import praw
import os
import time

def fail_and_exit(err_str):
	print err_str
	sys.exit(1)

parser = argparse.ArgumentParser(description='Shopbot automates your reddit shopping experience!')
parser.add_argument('--pm', action='store_true', help='Notify via Reddit pm (default: notify via Twilio)')
args = parser.parse_args()
should_pm = args.pm

if config.client_id == '' or config.client_id is None:
	fail_and_exit("client_id configuration is empty.")
if config.client_secret == '' or config.client_secret is None:
	fail_and_exit("client_secret configuration is empty.")
if config.username == '' or config.username is None:
	fail_and_exit("username configuration is empty.")
if config.password == '' or config.password is None:
	fail_and_exit("password configuration is empty.")
if config.user_agent == '' or config.user_agent is None:
	fail_and_exit("user_agent configuration is empty.")

if config.bitly_token == '' or config.bitly_token is None:
	print 'Bit.ly token not provided! Long URLs will be included in output.'

if not should_pm:
	print "You provided the private message flag but did not provide a Twilio configuration variable."
	if config.account_sid == '' or config.account_sid is None:
		fail_and_exit("account_sid configuration is empty.")
	if config.auth_token == '' or config.auth_token is None:
		fail_and_exit("auth_token configuration is empty.")
	if config.sms_sender == '' or config.sms_sender is None:
		fail_and_exit("sms_Sender configuration is empty")
	if config.sms_recipient == '' or config.sms_recipient is None:
		fail_and_exit("sms_recipient configuration is empty.")

reddit = praw.Reddit(client_id 	   = config.client_id,
		     client_secret = config.client_secret,
		     username 	   = config.username,
		     password 	   = config.password,
		     user_agent    = config.user_agent)

should_notify = shopbot.parse(reddit)
if should_notify:
	notify.notify(should_pm, reddit)
	os.remove('found.json')
else:
	print "Did not find any items you are interested in buying or selling."

with open('shopbot.last_run', 'w+') as last_run:
	# cast to int to get rid of decimal part
	last_run.write(str(int(time.time())))
