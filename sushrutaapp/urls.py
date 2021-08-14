from django.urls import path
from . import views


urlpatterns = [
    path('', views.reg, name='reg'),
    path('/login', views.login, name='login'),
]
