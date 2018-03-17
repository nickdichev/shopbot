# mk-helper

This project helps you find items you want to buy and sell online. In particular, it helps you parse "shopping" Reddit pages that use the [H][W][L] tags (have, want, location) in the post's title. The script utilizes the PRAW (Python Reddit API Wrapper) API to parse posts for items you want to buy or sell on subreddits that you choose. 

## Dependencies 
Python 2.7
PRAW -- `pip install praw`

## PRAW app setup
Browse to your Reddit account's `preferences>apps` page. Scroll to the bottom and select "create another app..." .  Give your app a name and description and use `http://www.example.com/unused/redirect/uri` as your "redirect URI". Finally, select the type `script` for your app. Click "create app".

Make note of your newly created app's `client_id` and `client_secret` as they will be needed to fill out the config file. 

## Configuration
#### Reddit PRAW configuration
Rename `config_template.py` to `config.py` and fill out the "RedditPRAW" configuration section. You will use the `client_id` and `client_secret` from the above section. The `username` and `password` configuration settings are the credentials for the Reddit account that you created the Reddit app with. Finally, make a `user_agent` with the format ``<platform>:<app ID>:<version string> (by /u/<Reddit username>)``. 

### Subreddit Shopping configuration
The `subreddit_dict` dictionary is used to where and what items to look for. Each item in the dictionary is a dictionary that contains two keys: `wanted_items` and `owned_items`. Each of these keys map to a list of strings that are the items you want to buy and the items you want to sell, respectively.  An example is provided in `config_template.py`. 

## Running shopbot
Use `python shopbot.py` to run the script. The script currently prints the username and the associated Subreddit for your desired items. The script also creates an output file `out.json`. I plan to write an additional script that reads this file and will notify my via Twilio or Reddit private message. 

## Deployment
Currently I run this script on my machine locally, however, I can easily see this script (and the associated notification script) running on a cheap VPS with a cron job. 

