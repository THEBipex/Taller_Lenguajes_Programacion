from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  TallerViewSet, talleres_disponibles, home

router = DefaultRouter()
router.register(r'talleres', TallerViewSet, basename='talleres')

urlpatterns = [
    path('', home, name='home'),
    path('talleres/', talleres_disponibles, name='talleres_disponibles'),
    path('api/', include(router.urls)),
]