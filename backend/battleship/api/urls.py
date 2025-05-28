from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from . import views
from .views import PlayerViewSet, GameViewSet, UserViewSet, BoardViewSet, VesselViewSet, BoardVesselViewSet, ShotViewSet

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'games', GameViewSet)
router.register(r'boards', BoardViewSet)
router.register(r'vessels', VesselViewSet)
router.register(r'boardvessels', BoardVesselViewSet)
router.register(r'shots', ShotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

