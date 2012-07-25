from coffee.models import *
from django.db.models import Count, Sum
import datetime

def drink_coffee(twitter_name,quantity=1):
    usr, created = CoffeeUser.objects.get_or_create(twitter_name=twitter_name)
    if created:
        usr.user_name = twitter_name
    usr.drink(quantity=quantity)
    usr.save()

def top_up_credit(twitter_name,quantity):
    usr, created = CoffeeUser.objects.get_or_create(twitter_name=twitter_name)
    if created:
        usr.user_name = twitter_name
    usr.top_up(quantity=quantity)
    usr.save()

def change_user_name(twitter_name,user_name):
    usr, created = CoffeeUser.objects.get_or_create(twitter_name=twitter_name)
    usr.user_name = user_name
    usr.save()

def get_balance(twitter_name):
    usr = CoffeeUser.objects.get(twitter_name=twitter_name)
    if usr is None:
        print "User %s does not exists" % (twitter_name,) 
    return usr.balance

def get_user_name(twitter_name):
    usr = CoffeeUser.objects.get(twitter_name=twitter_name)
    if usr is None:
        print "User %s does not exists" % (twitter_name,) 
    return usr.user_name

def get_last_processed_tweet():
    return CoffeeConfig.get().last_processed_tweet

def set_last_processed_tweet(tweet_id):
    c = CoffeeConfig.get()
    c.last_processed_tweet = tweet_id
    c.save()

def get_overall_coffees_amount():
    return CoffeeTransaction.objects.filter(operation=Operation.Drink).aggregate(Sum('amount'))['amount__sum']

def get_todays_coffees_amount():
    d = datetime.date.today()
    return CoffeeTransaction.objects.filter(operation=Operation.Drink,
                                            coffee_date__year=d.year,
                                            coffee_date__month=d.month,
                                            coffee_date__day=d.day
                                        ).aggregate(Sum('amount'))['amount__sum']

def get_month_coffees_amount():
    d = datetime.date.today()
    return CoffeeTransaction.objects.filter(operation=Operation.Drink,
                                            coffee_date__year=d.year,
                                            coffee_date__month=d.month
                                        ).aggregate(Sum('amount'))['amount__sum']

def get_top_drinker_names():
    top_id = CoffeeTransaction.objects.filter(operation=Operation.Drink).values('coffee_user').annotate(Count('amount')).order_by('-amount__count')[0]['coffee_user']
    top_user = CoffeeUser.objects.get(id=top_id)
    return top_user.user_name, top_user.twitter_name

def get_month_coffees():
    d = datetime.date.today()
    q = CoffeeTransaction.objects.filter(operation=Operation.Drink,
                                        coffee_date__year=d.year,
                                        coffee_date__month=d.month)
    # q.extra({'d':"strftime('%%d', date)"}).values('d').annotate(Sum('amount'))
                                        #.extra(select={'day':"strftime('%%d', date)"}).values('day')
    print q

    return q

def get_last_updated():
    return CoffeeConfig.get().last_updated
