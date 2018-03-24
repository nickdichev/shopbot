import json
import praw
import config
import time
import re
from datetime import datetime, timedelta, date
from bitly import get_short_url

def json_serial(obj):
	"""JSON serializer to encode datetime as strings"""

	if isinstance(obj, (datetime, date)):
		return obj.isoformat()
	return obj
	# raise TypeError ("Type %s not serializable" % type(obj))

def parse(reddit):
	location_re = re.compile('\[(\S*)\]')
	# need to find regex that does not grab trailing space here
	has_re = re.compile('\[H\] ?([^\[]*)') # [H] ?["0 or more not [""]
	wants_re = re.compile('\[W\] ?(.*)') # [W] ?["0 or more not new line"]

	found_post_count = 0
	found_posts = []
	start_time = date.today() - timedelta(days=1)

	output_data = []

	for curr_subreddit in config.subreddit_dict:
		subreddit = reddit.subreddit(curr_subreddit)
		for submission in subreddit.submissions(start=datetime.strftime(start_time, '%s')):
		    title = submission.title

		    location = has = wants = None
		    if location_re.search(title):
			location = location_re.search(title).group(0)
		    if has_re.search(title):
			has = has_re.search(title).group(1)
		    if wants_re.search(title):
			wants = wants_re.search(title).group(1)

		    if has is not None:
			has = has.lower()
		    if wants is not None:
			wants = wants.lower()

		    post_info = {
			'author' : submission.author.name,
			'date' : datetime.fromtimestamp(submission.created),
			'title' : submission.title,
			'body' : submission.selftext,
			'url' : submission.url,
			'location' : location,
			'has' : has,
			'wants': wants,
		    }
		    found_posts.append(post_info)
		    found_post_count += 1

		# print 'Processed {} submissions in {}'.format(found_post_count, curr_subreddit)

		wanted_items = config.subreddit_dict[curr_subreddit]["wanted_items"]
		owned_items = config.subreddit_dict[curr_subreddit]["owned_items"]
		
		wanted_items = [_.lower() for _ in wanted_items]
		owned_items = [_.lower() for _ in owned_items]

		subreddit_output_data = { 
			curr_subreddit : {
				"wanted_items_post_list": [], 
				"owned_items_post_list": []
			} 
		}

		for post in found_posts:
		    for wanted_item in wanted_items:
			try :
			    if wanted_item in post['has'] or wanted_item in post['body']:
				# print 'user {} has an item you want'.format(post['author'])
				post['url'] = get_short_url(post['url'])
				subreddit_output_data[curr_subreddit]["wanted_items_post_list"].append(post)
			except:
			    pass

		    for owned_item in owned_items:
			try:
			    if owned_item in post['wants']:
				# print 'user {} wants an item you have'.format(post['author'])
				post['url'] = get_short_url(post['url'])
				subreddit_output_data[curr_subreddit]["owned_items_post_list"].append(post)
			except:
			    pass

		output_data.append(subreddit_output_data)

	with open("found.json", "w+") as outfile:
		outfile.write(json.dumps(output_data, default=json_serial))
