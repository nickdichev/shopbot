import requests
import config
import urllib
import re

def get_short_url(long_url):
	# don't shorten bit.ly URLs or if config doens't have a token
	if re.match('https?://bit.ly', long_url) or config.bitly_token == '' or config.bitly_token is None:
		return long_url 
	encoded_url = urllib.quote(long_url, safe='')
	r = requests.get('https://api-ssl.bitly.com/v3/shorten?access_token={}&longUrl={}&format=txt'.format(config.bitly_token, encoded_url))
	return r.text
