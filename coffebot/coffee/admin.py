from django.contrib import admin
from coffee.models import CoffeeUser, CoffeeTransaction

admin.site.register(CoffeeUser)
admin.site.register(CoffeeTransaction)