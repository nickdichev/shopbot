import json
import config
from twilio.rest import Client
from pprint import pprint as pp

text_output = ''

with open('found.json', 'r') as infile:
	found_items = json.load(infile)

	for subreddit_dict in found_items:
		for subreddit in subreddit_dict:
			wanted_key = 'wanted_items_post_list'
			owned_key = 'owned_items_post_list'
			wanted_list = subreddit_dict[subreddit][wanted_key]
			owned_list = subreddit_dict[subreddit][owned_key]
			for post in wanted_list:
				text_output += '{}: /u/{} has an item you want! {}'.format(subreddit, post['author'], post['url'])
			for post in owned_list:
				text_output += '{}: /u/{} wants an item you have! {}'.format(subreddit, post['author'], post['url'])

print(text_output)

twilio_client = Client(config.account_sid, config.auth_token)


twilio_client.api.account.messages.create(
	to    = config.sms_recipient,
	from_ = config.sms_sender,
	body  = text_output)
