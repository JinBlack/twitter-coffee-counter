from twitter.api import Twitter, TwitterError
from twitter.oauth import OAuth, write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

import time
import sys
import re

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coffebot.settings")

from coffee.views import drink_coffee, change_user_name, top_up_credit

#REGEX
DRINK_COFFEE_REGEX = r"(\d*)\s?#(coffee)"
TOP_UP_CREDIT_REGEX = r"#(topup) ([1-9]\d*)"
CHANGE_NAME_REGEX = r"#(mynameis) (\w{3,})"

DRINK_COFFEE_MATCHER = re.compile(DRINK_COFFEE_REGEX)
TOP_UP_MATCHER = re.compile(TOP_UP_CREDIT_REGEX)
CHANGE_NAME_MATCHER = re.compile(CHANGE_NAME_REGEX)

CONSUMER_KEY='Mkl3Gy8PDEK4ltFi8L2dag'
CONSUMER_SECRET='0wL5STrR76fzmuNlq491WRHpgYWi0pkgAIww3tTVQ'
TWITTER_CREDS = os.path.expanduser('~/.ncbot_twitter_oauth')
if not os.path.exists(TWITTER_CREDS):
    oauth_dance("NCBot", CONSUMER_KEY, CONSUMER_SECRET,
                TWITTER_CREDS)


# The very first arg, if present, is the last id replied to.

if __name__ == '__main__':
    oauth_token, oauth_token_secret = read_token_file(TWITTER_CREDS)

    # We use two twitter clients, one to search, another to update. Just
    # easier that way...
    twitter = Twitter(domain='search.twitter.com')
    twitter.uriparts=()

    last_id_replied = ''

    print '###### args = ', sys.argv

    if len(sys.argv) > 1:
        last_id_replied = sys.argv[1]

    poster = Twitter(
        auth=OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
        secure=True,
        api_version='1',
        domain='api.twitter.com')

    while True:
        results = twitter.search(q="@NCBot", 
                    since_id=last_id_replied)['results']
    
        if not results:
            print 'No results this time...'

        for result in results:
            # Remove my name from the question.
            tweet = result['text'].replace('@NCBot', '')
            from_user = result['from_user']
            id = str(result['id'])
            print " <<< " + from_user + ": " + tweet
            
            #Parse tweet and select action
            # u = CoffeeUser.objects.get_or_create(from_user).drink()
            # u.save()

            m = DRINK_COFFEE_MATCHER.search(tweet)
            if m is not None:
                groups = m.groups()
                n_coffees = 1 if groups[0] == '' else int(groups[0])
                drink_coffee(from_user, n_coffees)
            else:
                m = TOP_UP_MATCHER.search(tweet)
                if m is not None:
                    groups = m.groups()
                    top_up_credit(from_user, int(groups[1]))
                else:
                    m = CHANGE_NAME_MATCHER.search(tweet)
                    if m is not None:
                        groups = m.groups()
                        change_user_name(from_user, groups[1])
                    else:
                        continue


            #TODO Send response msg

            # We append part of the ID to avoid duplicates.
            # msg = '@%s %s (%s)' % (from_user, doctor_response, id[-4:])
            # print '====> Resp = %s' % msg
            last_id_replied = id
            # poster.statuses.update(status=msg)
            print 'Last id replied = ', last_id_replied

        print 'Now sleeping... \n\n'
        time.sleep(3)
