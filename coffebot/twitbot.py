from twitter.api import Twitter, TwitterError
from twitter.oauth import OAuth, write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

import sys
import re

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coffebot.settings")

from coffee.views import *

import time

# PARAMS
POLLING_INTERVAL_SECONDS = 30 # NOTE: Twitter limits unauthenticated REST API calls to 150/h, i.e. 2,5/m
BOT_NAME = "@NCBot"

# REGEXES
DRINK_COFFEE_REGEX = r"(\d*)\s?#coffee"
TOP_UP_CREDIT_REGEX = r"#topup ([1-9]\d*)"
CHANGE_NAME_REGEX = r"#mynameis (\w{3,})"
INQUIRE_BALANCE_REGEX = r"#howmany"

# MATCHERS
DRINK_COFFEE_MATCHER = re.compile(DRINK_COFFEE_REGEX)
TOP_UP_MATCHER = re.compile(TOP_UP_CREDIT_REGEX)
CHANGE_NAME_MATCHER = re.compile(CHANGE_NAME_REGEX)
INQUIRE_BALANCE_MATCHER = re.compile(INQUIRE_BALANCE_REGEX)

# TWITTER OAUTH
CONSUMER_KEY='Mkl3Gy8PDEK4ltFi8L2dag'
CONSUMER_SECRET='0wL5STrR76fzmuNlq491WRHpgYWi0pkgAIww3tTVQ'
TWITTER_CREDS = os.path.expanduser('~/.ncbot_twitter_oauth')
if not os.path.exists(TWITTER_CREDS):
    oauth_dance("NCBot", CONSUMER_KEY, CONSUMER_SECRET,
                TWITTER_CREDS)


def dispatch_action(tweet):
    m = DRINK_COFFEE_MATCHER.search(tweet)
    if m is not None:
        groups = m.groups()
        n_coffees = 1 if groups[0] == '' else int(groups[0])
        drink_coffee(from_user, n_coffees)
        msg = 'Enjoy your coffee! Your balance is %i' % (get_balance(from_user),)
        return msg

    m = TOP_UP_MATCHER.search(tweet)
    if m is not None:
        groups = m.groups()
        top_up_credit(from_user, int(groups[0]))
        msg = 'Hi %s! Your balance is %i' % (get_user_name(from_user), get_balance(from_user),)
        return msg

    m = CHANGE_NAME_MATCHER.search(tweet)
    if m is not None:
        groups = m.groups()
        change_user_name(from_user, groups[0])
        msg = 'Hi %s! Your balance is %i' % (groups[0], get_balance(from_user),)
        return msg

    m = INQUIRE_BALANCE_MATCHER.search(tweet)
    if m is not None:
        msg = 'Hi %s! Your balance is %i' % (get_user_name(from_user), get_balance(from_user),)
        return msg

    return None


# The very first arg, if present, is the last id replied to.
if __name__ == '__main__':
    oauth_token, oauth_token_secret = read_token_file(TWITTER_CREDS)

    # We use two twitter clients, one to search, another to update.
    twitter = Twitter(domain='search.twitter.com')
    twitter.uriparts=()
    # The authenticated twitter account used to reply
    poster = Twitter(
        auth=OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
        secure=True,
        api_version='1',
        domain='api.twitter.com')

    last_id_replied = get_last_processed_tweet()
    if len(sys.argv) > 1:
        last_id_replied = sys.argv[1]

    while True:
        try:
            results = twitter.search(q=BOT_NAME, 
                        since_id=last_id_replied)['results']
        
            if not results:
                print 'No results this time...'

            # reverse the results in order to process them in ascending timestamp 
            for result in reversed(results):
                # Remove bot name from the tweet.
                tweet = result['text'].replace(BOT_NAME, '')
                from_user = result['from_user']
                id = str(result['id'])
                print " <<< " + from_user + ": " + tweet
                
                response = dispatch_action(tweet)
                # attach part of the id to avoid duplicates
                msg = "%s (#%s)" % (response, id[-4:])

                # reply via PM
                if response is not None:
                    poster.direct_messages.new(
                            user=from_user,
                            text=msg)

                # keep trace of the last processed tweet
                last_id_replied = id
                set_last_processed_tweet(id)
        except TwitterError as te:
            print te

        print 'Now sleeping... \n\n'
        time.sleep(POLLING_INTERVAL_SECONDS)

