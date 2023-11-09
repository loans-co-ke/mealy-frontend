from rest_framework_nested import routers

from .  import views

router = routers.DefaultRouter()

router.register('meals', views.MealViewSet, basename='meals')
router.register('menus', views.MenuViewSet, basename='menus')
router.register('admins', views.AdminViewSet, basename='admins')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('orders', views.OrderViewSet, basename='orders')

urlpatterns = router.urls