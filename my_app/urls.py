from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_check', views.new_check, name='new_check'),
]
