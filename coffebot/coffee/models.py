from django.db import models

class Operation(DjangoChoices):
	TopUp = ChoiceItem('TOP')
	Drink = ChoiceItem('DRK')


# Create your models here.
class CoffeeUser(models.Model):
	user_name = models.CharField(max_length=50, unique=True, null=False)
	twitter_name = models.CharField(max_length=50, unique=True, null=False)
# TODO Create a custom validator for both the above field
	total_coffees = models.PositiveIntegerField(default=0, null=False)
	balance = models.IntegerField(default=0, null=False)

	@classmethod
    def create(cls, user_name, twitter_name):
        coffee_user = cls(user_name=user_name, twitter_name=twitter_name)
        return coffee_user

	def drink(self, quantity=1):
		self.total_coffees += quantity
		self.balance -= quantity
		CoffeeTransaction.create(Operation.Drink, quantity)

	def top_up(self, quantity):
		self.balance += quantity
		CoffeeTransaction.create(Operation.TopUp, quantity)

	def change_user_name(self, name):
		self.user_name = name

class CoffeeTransaction(models.Model):
	date = models.DateField(auto_now_add=True, null=False)
	operation = models.CharField(max_length=3, choices=Operation.choices, null=False)
	amount = models.PositiveIntegerField(default=1)

	@classmethod
    def create(cls, operation, amount):
        transaction = cls(operation=operation, amount=amount)
        return transaction

