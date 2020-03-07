from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import ContactViewSet, MessageViewSet

routers = routers.DefaultRouter()
routers.register('contacts', ContactViewSet)
routers.register('messages', MessageViewSet)

urlpatterns = [
    path('', include(routers.urls)),
]
