import argparse
import shopbot
import notify
import config
import sys
import praw
import os

def fail_and_exit(err_str):
	print err_str
	sys.exit(1)

parser = argparse.ArgumentParser(description='Shopbot automates your reddit shopping experience!')
parser.add_argument('--pm', action='store_true', help='Notify via Reddit pm (default: notify via Twilio)')
args = parser.parse_args()

if config.client_id == '' or config.client_id is None:
	fail_and_exit("client_id configuration is empty")
if config.client_secret == '' or config.client_secret is None:
	fail_and_exit("client_secret configuration is empty")
if config.username == '' or config.username is None:
	fail_and_exit("username configuration is empty")
if config.password == '' or config.password is None:
	fail_and_exit("password configuration is empty")
if config.user_agent == '' or config.user_agent is None:
	fail_and_exit("user_agent configuration is empty")

if config.bitly_token == '' or config.bitly_token is None:
	args.pm = True

if not args.pm:
	if config.account_sid == '' or config.account_sid is None:
		fail_and_exit("account_sid configuration is empty")
	if config.auth_token == '' or config.auth_token is None:
		fail_and_exit("auth_token configuration is empty")
	if config.sms_sender == '' or config.sms_sender is None:
		fail_and_exit("sms_Sender configuration is empty")
	if config.sms_recipient == '' or config.sms_recipient is None:
		fail_and_exit("sms_recipient configuration is empty")

reddit = praw.Reddit(client_id = config.client_id,
		     client_secret = config.client_secret,
		     username = config.username,
		     password = config.password,
		     user_agent = config.user_agent)

shopbot.parse(reddit)
notify.notify(args.pm, reddit)
os.remove('found.json')
