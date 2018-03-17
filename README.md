# shopbot

This project helps you find items you want to buy and sell online. In particular, it helps you parse "shopping" Reddit pages that use the [H][W][L] tags (have, want, location) in the post's title. The script utilizes the PRAW (Python Reddit API Wrapper) API to parse posts for items you want to buy or sell on subreddits that you choose. The Twilio API is used to facilitate sending SMS messages.

## Dependencies 
Python 2.7

PRAW -- `pip install praw`

Twilio -- `pip install twilio`

## Setup
#### PRAW
Browse to your Reddit account's `preferences>apps` page. Scroll to the bottom and select "create another app..." .  Give your app a name and description and use `http://www.example.com/unused/redirect/uri` as your "redirect URI". Finally, select the type `script` for your app. Click "create app".

Make note of your newly created app's `client_id` and `client_secret` as they will be needed to fill out the config file. 

#### Twilio [optional]
Setup Twilio for programable SMS. You will need to purchase a phone number and add credits to your account. Find your `account_sid` and `auth_token` in the "Programmable SMS" section of your account. These fields will be required in the configuration file. If you do not want to use Twilio you must provide the `--pm` flag when you run the program. 

#### Bit.ly [optional]
Create a bit.ly account and generate an access token. Navigate to your "Account Profile" and select "Generic Access Token". This is the token that you will put in the configuration file. Note that if you do not supply this field in the configuration file there will be long URLs in the output. 

## Configuration
Rename `config_template.py` to `config.py` and fill out the configuration fields.

#### PRAW
You will use the `client_id` and `client_secret` from the PRAW setup section. The `username` and `password` configuration settings are the credentials for the Reddit account that you created the Reddit app with. Finally, set `user_agent` with the format `<platform>:<app ID>:<version string> (by /u/<Reddit username>)`. 

#### Subreddit Shopping
The `subreddit_dict` dictionary is used to where and what items to look for. Each item in the dictionary is a dictionary that contains two keys: `wanted_items` and `owned_items`. Each of these keys map to a list of strings that are the items you want to buy and the items you want to sell, respectively.  An example is provided in `config_template.py`. 

#### Twilio [optional]
The two fields that come from your Twilio account are `account_sid` and `auth_token`. The `sms_sender` and `sms_recipient` fields expect the form '+<country code><area code><phone number>' eg. '+14561234567'

#### Bit.ly [optional]
The only field is `bitly_token` which is optional, however, it is highly recommended. 

## Usage
Use `python main.py` to run the script. The program notifies via Twilio by default, however, you can set the `--pm` flag to send the output via private message to the username set in the configuration file.
```
usage: main.py [-h] [--pm]

Shopbot automates your reddit shopping experience!

optional arguments:
  -h, --help  show this help message and exit
  --pm        Notify via Reddit pm (default: notify via Twilio)
```

## Deployment
Currently I run this project on my machine locally, however, I intend to run this on a cheap VPS with a cron job. 

