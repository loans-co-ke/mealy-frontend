from django.contrib import admin
from .models import Admin, Customer, Menu, Meal, Order

admin.site.register(Admin)
admin.site.register(Customer)
admin.site.register(Menu)
admin.site.register(Meal)
admin.site.register(Order)
