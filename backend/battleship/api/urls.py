from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from . import views
from .views import PlayerViewSet, GameViewSet, UserViewSet

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'games', GameViewSet)
router.register(r'boards', views.BoardViewSet)
router.register(r'vessels', views.VesselViewSet)
router.register(r'boardvessels', views.BoardVesselViewSet)
router.register(r'shots', views.ShotViewSet)

urlpatterns = [
    path('', include(router.urls))
]