import praw
import config
import time
import re
from pprint import pprint
from datetime import datetime, timedelta, date

reddit = praw.Reddit(client_id = config.client_id,
                     client_secret = config.client_secret,
                     username = config.username,
                     password = config.password,
                     user_agent = config.user_agent)

location_re = re.compile('\[(\S*)\]')
# need to find regex that does not grab trailing space here
has_re = re.compile('\[H\] ?([^\[]*)') # [H] ?["0 or more not [""]
wants_re = re.compile('\[W\] ?(.*)') # [W] ?["0 or more not new line"]

found_post_count = 0
found_posts = []
start_time = date.today() - timedelta(days=1)

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
		'body' : submission.selftext,
		'location' : location,
		'has' : has,
		'wants': wants,
	    }
	    found_posts.append(post_info)
	    found_post_count += 1

	print 'Processed {} submissions in {}'.format(found_post_count, curr_subreddit)

	wanted_items = config.subreddit_dict[curr_subreddit]["wanted_items"]
	owned_items = config.subreddit_dict[curr_subreddit]["owned_items"]

	for post in found_posts:
	    for wanted_item in wanted_items:
		try :
		    if wanted_item in post['has'] or wanted_item in post['body']:
			print 'user {} has an item you want'.format(post['author'])
		except:
		    pass

	    for owned_item in owned_items:
		try:
		    if owned_item in post['wants']:
			print 'user {} wants an item you have'.format(post['author'])
		except:
		    pass
