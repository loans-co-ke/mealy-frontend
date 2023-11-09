from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions

from .permissions import IsSysAdmin, IsCustomer
from .models import Customer, Admin, Meal, Menu, Order
from .serializers import (
    CustomerSerializer, AdminSerializer,
    MealSerializer, MenuSerializer,
    OrderSerializer, AddOrderSerializer,
    CreateMenuSerializer
)

class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class MealViewSet(ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    search_fields = ['name']

class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PATCH']:
            return [IsSysAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_context(self):
        return {
            'admin_id': self.request.user.id
        }
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateMenuSerializer
        return MenuSerializer
    
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsCustomer()]
        return [permissions.IsAuthenticated()]

    def get_serializer_context(self):
        return {
            'customer_id': self.request.user.id
        }
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddOrderSerializer
        return OrderSerializer

    