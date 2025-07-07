from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  TallerViewSet, talleres_disponibles, home
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

router = DefaultRouter()
router.register(r'talleres', TallerViewSet, basename='talleres')

urlpatterns = [
    path('', home, name='home'),
    path('talleres/', talleres_disponibles, name='talleres_disponibles'),
    path('api/', include(router.urls)),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]