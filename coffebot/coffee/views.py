from coffee.models import *

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