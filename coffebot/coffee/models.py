from django.db import models
from djchoices import *

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
        t = CoffeeTransaction.create(self, Operation.Drink, quantity)
        t.save()

    def top_up(self, quantity):
        self.balance += quantity
        t = CoffeeTransaction.create(self, Operation.TopUp, quantity)
        t.save()

    def change_user_name(self, name):
        self.user_name = name

    def __unicode__(self):
        return self.user_name

class CoffeeTransaction(models.Model):
    coffee_user = models.ForeignKey('CoffeeUser', on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True, null=False)
    operation = models.CharField(max_length=3, choices=Operation.choices, null=False)
    amount = models.PositiveIntegerField(default=1)

    @classmethod
    def create(cls, user, operation, amount):
        transaction = cls(coffee_user=user, operation=operation, amount=amount)
        return transaction


