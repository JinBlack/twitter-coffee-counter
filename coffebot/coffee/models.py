from django.db import models

# Create your models here.
class CoffeeUser(models.Model):
	user_name = models.CharField(max_lenght=50, unique=True, null=False)
	twitter_name = models.CharField(max_length=50, unique=True, null=False)
# Create a custom validator for both the above field
	total_coffees = models.PositiveIntegerField(default=0, null=False)
	balance = models.IntegerField(default=0, null=False)

	@classmethod
    def create(cls, user_name, twitter_name):
        coffee_user = cls(user_name=user_name, twitter_name=twitter_name)
        # do something with the book
        return coffee_user

	def drink(self, quantity=1):
		self.total_coffees += quantity
		self.balance -= quantity

	def top_up(self, quantity):
		self.balance += quantity

	def change_user_name(self, name):
		self.user_name = name

