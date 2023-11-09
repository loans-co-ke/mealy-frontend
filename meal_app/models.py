from django.db import models
from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator

class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    @admin.display(ordering='user__username')
    def username(self):
        return self.user.username
    
    class Meta:
        db_table = 'admins'
        verbose_name_plural = 'Admins'
        ordering = ['user__first_name', 'user__last_name']

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    @admin.display(ordering='user__username')
    def username(self):
        return self.user.username
    
    class Meta:
        db_table = 'customers'
        verbose_name_plural = 'Customers'
        ordering = ['user__first_name', 'user__last_name']

class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(blank=True, upload_to='meal_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'meals'
        verbose_name_plural = 'Meals'

    def __str__(self):
        return self.name
    
class Menu(models.Model):
    created_by = models.ForeignKey(Admin, on_delete=models.CASCADE)
    menu_meals = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='meals')
    date = models.DateField()
    
    class Meta:
        db_table = 'menu'

# class MenuMeal(models.Model):
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='meals')
#     meals = models.ForeignKey(Meal, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'menu_meals'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    chosen_meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'{self.customer.first_name()}'
    
# class OrderMeal(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='meals')


