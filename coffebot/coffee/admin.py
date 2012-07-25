from django.contrib import admin
from singleton_models.admin import SingletonModelAdmin
from coffee.models import CoffeeUser, CoffeeTransaction, CoffeeConfig

admin.site.register(CoffeeUser)
admin.site.register(CoffeeTransaction)
admin.site.register(CoffeeConfig)